param(
	[switch]$SkipLaunch
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# Versions validées pour cette révision de PALM Tracer.
$CompatiblePythonVersion = [version]"3.14.7"
$MinimumPythonVersion = [version]"3.9.0"
$PalmTracerScmVersion = "1.4.0"
$PythonInstallerSha256 = "9D9EB2709EF81BF5CD30DB3C2096BDBC4EA10087C22E62F27D356B36F6AE9649"
$PythonInstallerUrl = "https://www.python.org/ftp/python/$CompatiblePythonVersion/python-$CompatiblePythonVersion-amd64.exe"
$BuildToolsUrl = "https://aka.ms/vs/stable/vs_buildtools.exe"
$TutorialUrl = "https://tmonseigne.github.io/palm-tracer/user/install.html"
$ProjectPath = $PSScriptRoot
$TemporaryPath = Join-Path ([IO.Path]::GetTempPath()) "PalmTracerInstaller"
$LogPath = Join-Path ([IO.Path]::GetTempPath()) "palm-tracer-install.log"

# Force TLS 1.2 pour les anciennes configurations de Windows PowerShell 5.1.
[Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor
	[Net.SecurityProtocolType]::Tls12

function Show-Step {
	<#
	.SYNOPSIS
		Affiche le titre d'une étape de l'installation.
	#>
	param(
		[Parameter(Mandatory)]
		[int]$Number,

		[Parameter(Mandatory)]
		[string]$Message
	)

	Write-Host ""
	Write-Host "[$Number/6] $Message" -ForegroundColor Cyan
}

function Test-Administrator {
	<#
	.SYNOPSIS
		Indique si le processus courant possède les droits administrateur.
	#>
	$identity = [Security.Principal.WindowsIdentity]::GetCurrent()
	$principal = [Security.Principal.WindowsPrincipal]::new($identity)
	return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Start-ElevatedInstaller {
	<#
	.SYNOPSIS
		Relance l'installeur avec une demande d'élévation UAC.
	#>
	Write-Host "Administrator privileges are required. Please accept the Windows UAC prompt."
	$arguments = @(
		"-NoProfile",
		"-ExecutionPolicy", "Bypass",
		"-File", "`"$PSCommandPath`""
	)
	if ($SkipLaunch) {
		$arguments += "-SkipLaunch"
	}

	Start-Process -FilePath "powershell.exe" -ArgumentList $arguments -Verb RunAs | Out-Null
}

function Add-PythonCandidate {
	<#
	.SYNOPSIS
		Ajoute un chemin Python potentiel à une collection sans doublon.
	#>
	param(
		[Parameter(Mandatory)]
		[AllowEmptyCollection()]
		[Collections.Generic.HashSet[string]]$Paths,

		[AllowNull()]
		[string]$Path
	)

	if ([string]::IsNullOrWhiteSpace($Path)) { return }
	if ($Path -like "*\Microsoft\WindowsApps\*") { return } # Ignore les alias Windows Store.
	if (Test-Path -LiteralPath $Path -PathType Leaf) { [void]$Paths.Add([IO.Path]::GetFullPath($Path)) }
}

function Get-PythonCandidates {
	<#
	.SYNOPSIS
		Détecte les installations Python utilisables et les trie par version décroissante.
	#>
	$paths = [Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)

	Get-Command python.exe -CommandType Application -All -ErrorAction SilentlyContinue |
		ForEach-Object { Add-PythonCandidate -Paths $paths -Path $_.Source }

	$launcher = Get-Command py.exe -CommandType Application -ErrorAction SilentlyContinue |
		Select-Object -First 1
	if ($null -ne $launcher) {
		try {
			$launcherOutput = & $launcher.Source -0p 2>$null
			if ($LASTEXITCODE -eq 0) {
				foreach ($line in $launcherOutput) {
					$match = [regex]::Match($line, "(?<path>[A-Za-z]:\\.+\\python(?:w)?\.exe)\s*$", [Text.RegularExpressions.RegexOptions]::IgnoreCase)
					if ($match.Success) { Add-PythonCandidate -Paths $paths -Path $match.Groups["path"].Value }
				}
			}
		}
		catch { } # Un lanceur incomplet ou obsolète ne doit pas bloquer les autres méthodes.
	}

	$registryRoots = @(
		"Registry::HKEY_LOCAL_MACHINE\SOFTWARE\Python\PythonCore",
		"Registry::HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Python\PythonCore",
		"Registry::HKEY_CURRENT_USER\SOFTWARE\Python\PythonCore"
	)
	foreach ($registryRoot in $registryRoots) {
		if (-not (Test-Path -LiteralPath $registryRoot)) { continue }

		Get-ChildItem -LiteralPath $registryRoot -ErrorAction SilentlyContinue | ForEach-Object {
			$installationPath = $_.GetValue("")
			if (-not [string]::IsNullOrWhiteSpace($installationPath)) { Add-PythonCandidate -Paths $paths -Path (Join-Path $installationPath "python.exe") }
		}
	}

	$commonRoots = @($env:ProgramFiles, (Join-Path $env:LocalAppData "Programs\Python"))
	foreach ($commonRoot in $commonRoots) {
		if (-not (Test-Path -LiteralPath $commonRoot)) { continue }

		Get-ChildItem -LiteralPath $commonRoot -Directory -Filter "Python*" -ErrorAction SilentlyContinue |
			ForEach-Object { Add-PythonCandidate -Paths $paths -Path (Join-Path $_.FullName "python.exe") }
	}

	$candidates = foreach ($path in $paths) {
		try {
			$description = & $path -c "import json, struct, sys; print(json.dumps({'version': list(sys.version_info[:3]), 'bits': struct.calcsize('P') * 8, 'path': sys.executable}))" 2>$null
			if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($description)) { continue }

			$data = $description | ConvertFrom-Json
			[pscustomobject]@{
				Path = [IO.Path]::GetFullPath([string]$data.path)
				Version = [version]("{0}.{1}.{2}" -f $data.version[0], $data.version[1], $data.version[2])
				Bits = [int]$data.bits
			}
		}
		catch { } # Les alias invalides et installations incomplètes sont ignorés.
	}

	return @($candidates | Sort-Object Version -Descending)
}

function Confirm-Choice {
	<#
	.SYNOPSIS
		Demande une confirmation avec une réponse positive par défaut.
	#>
	param(
		[Parameter(Mandatory)]
		[string]$Message
	)

	while ($true) {
		$answer = (Read-Host "$Message [Y/n]").Trim()
		if ([string]::IsNullOrWhiteSpace($answer) -or $answer -match "^[Yy]") { return $true }
		if ($answer -match "^[Nn]") { return $false }
		Write-Host "Please answer Y or N." -ForegroundColor Yellow
	}
}

function Test-DownloadedExecutable {
	<#
	.SYNOPSIS
		Vérifie la signature Authenticode d'un exécutable téléchargé.
	#>
	param(
		[Parameter(Mandatory)]
		[string]$Path,

		[Parameter(Mandatory)]
		[string]$ExpectedPublisher
	)

	$signature = Get-AuthenticodeSignature -LiteralPath $Path
	if ($signature.Status -ne [Management.Automation.SignatureStatus]::Valid -or
		$null -eq $signature.SignerCertificate -or
		$signature.SignerCertificate.Subject -notlike "*$ExpectedPublisher*") {
		throw "The digital signature of '$Path' is invalid or does not belong to $ExpectedPublisher."
	}
}

function Install-CompatiblePython {
	<#
	.SYNOPSIS
		Télécharge et installe silencieusement la version Python validée.
	#>
	New-Item -ItemType Directory -Path $TemporaryPath -Force | Out-Null
	$installerPath = Join-Path $TemporaryPath "python-$CompatiblePythonVersion-amd64.exe"
	Write-Host "Downloading Python $CompatiblePythonVersion from python.org..."
	Invoke-WebRequest -Uri $PythonInstallerUrl -OutFile $installerPath -UseBasicParsing

	$actualHash = (Get-FileHash -LiteralPath $installerPath -Algorithm SHA256).Hash
	if ($actualHash -ne $PythonInstallerSha256) { throw "The Python installer checksum is invalid. Expected $PythonInstallerSha256, received $actualHash." }
	Test-DownloadedExecutable -Path $installerPath -ExpectedPublisher "Python Software Foundation"

	Write-Host "Installing Python $CompatiblePythonVersion for all users. This may take several minutes..."
	$arguments = @("/quiet", "InstallAllUsers=1", "PrependPath=1", "Include_pip=1", "Include_launcher=1", "InstallLauncherAllUsers=1", "Include_dev=1", "Include_test=0")
	$process = Start-Process -FilePath $installerPath -ArgumentList $arguments -Wait -PassThru
	if ($process.ExitCode -notin @(0, 3010)) { throw "Python installation failed with exit code $($process.ExitCode)." }

	$env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" +
		[Environment]::GetEnvironmentVariable("Path", "User")
	$candidate = Get-PythonCandidates |
		Where-Object { $_.Bits -eq 64 -and $_.Version.Major -eq $CompatiblePythonVersion.Major -and $_.Version.Minor -eq $CompatiblePythonVersion.Minor } |
		Select-Object -First 1
	if ($null -eq $candidate) { throw "Python $CompatiblePythonVersion was installed but could not be detected. A Windows restart may be required." }

	return $candidate
}

function Select-Python {
	<#
	.SYNOPSIS
		Sélectionne la version Python la plus récente déclarée compatible.
	#>
	$candidates = @(Get-PythonCandidates)
	if ($candidates.Count -gt 0) {
		Write-Host "Detected Python installations:"
		$candidates | ForEach-Object { Write-Host "  - Python $($_.Version) ($($_.Bits)-bit): $($_.Path)" }
	}

	$targetSeries = @($candidates | Where-Object {
		$_.Bits -eq 64 -and
		$_.Version.Major -eq $CompatiblePythonVersion.Major -and
		$_.Version.Minor -eq $CompatiblePythonVersion.Minor
	})
	if ($targetSeries.Count -gt 0 -and $targetSeries[0].Version -ge $CompatiblePythonVersion) {
		Write-Host "Python $($targetSeries[0].Version) is compatible and up to date."
		return $targetSeries[0]
	}

	$supported = @($candidates | Where-Object {
		$_.Bits -eq 64 -and
		$_.Version -ge $MinimumPythonVersion -and
		($_.Version.Major -lt $CompatiblePythonVersion.Major -or
			($_.Version.Major -eq $CompatiblePythonVersion.Major -and $_.Version.Minor -le $CompatiblePythonVersion.Minor))
	})
	if ($supported.Count -gt 0) {
		$current = $supported[0]
		if (-not (Confirm-Choice "Python $($current.Version) is available. Install the recommended Python $CompatiblePythonVersion instead?")) {
			Write-Host "Continuing with Python $($current.Version)."
			return $current
		}
	}
	else { Write-Host "No compatible 64-bit Python installation was found." }

	return (Install-CompatiblePython)
}

function Get-VsWherePath {
	<#
	.SYNOPSIS
		Retourne le chemin standard de vswhere lorsqu'il est installé.
	#>
	$programFilesX86 = [Environment]::GetFolderPath([Environment+SpecialFolder]::ProgramFilesX86)
	$path = Join-Path $programFilesX86 "Microsoft Visual Studio\Installer\vswhere.exe"
	if (Test-Path -LiteralPath $path -PathType Leaf) { return $path }
	return $null
}

function Test-CppBuildTools {
	<#
	.SYNOPSIS
		Vérifie la présence des outils de compilation C++ x64/x86 de Visual Studio.
	#>
	$vsWherePath = Get-VsWherePath
	if ($null -eq $vsWherePath) { return $false }

	$installationPath = & $vsWherePath -latest -products "*" -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath 2>$null
	return $LASTEXITCODE -eq 0 -and -not [string]::IsNullOrWhiteSpace(($installationPath | Select-Object -First 1))
}

function Install-CppBuildTools {
	<#
	.SYNOPSIS
		Installe silencieusement la charge de travail C++ de Visual Studio Build Tools.
	#>
	if (Test-CppBuildTools) {
		Write-Host "Microsoft C++ Build Tools are already installed."
		return
	}

	New-Item -ItemType Directory -Path $TemporaryPath -Force | Out-Null
	$installerPath = Join-Path $TemporaryPath "vs_buildtools.exe"
	Write-Host "Downloading Microsoft Visual Studio Build Tools..."
	Invoke-WebRequest -Uri $BuildToolsUrl -OutFile $installerPath -UseBasicParsing
	Test-DownloadedExecutable -Path $installerPath -ExpectedPublisher "Microsoft Corporation"

	Write-Host "Installing Microsoft C++ Build Tools. This may take several minutes..."
	$arguments = @("--quiet", "--wait", "--norestart", "--nocache", "--add", "Microsoft.VisualStudio.Workload.VCTools","--includeRecommended")
	$process = Start-Process -FilePath $installerPath -ArgumentList $arguments -Wait -PassThru
	if ($process.ExitCode -notin @(0, 3010)) { throw "Microsoft Visual Studio Build Tools installation failed with exit code $($process.ExitCode)." }
	if (-not (Test-CppBuildTools)) { throw "Microsoft C++ Build Tools could not be detected after installation. A Windows restart may be required." }
}

function Install-PalmTracer {
	<#
	.SYNOPSIS
		Installe PALM Tracer et ses dépendances avec l'interpréteur sélectionné.
	#>
	param(
		[Parameter(Mandatory)]
		[string]$PythonPath
	)

	Write-Host "No virtual environment was created. PALM Tracer will be installed in the selected Python installation."
	& $PythonPath -m pip install --upgrade pip setuptools wheel
	if ($LASTEXITCODE -ne 0) { throw "pip, setuptools or wheel could not be updated." }

	$previousScmVersion = [Environment]::GetEnvironmentVariable("SETUPTOOLS_SCM_PRETEND_VERSION_FOR_PALM_TRACER", "Process")
	try {
		$env:SETUPTOOLS_SCM_PRETEND_VERSION_FOR_PALM_TRACER = $PalmTracerScmVersion
		& $PythonPath -m pip install -e "$ProjectPath[testing,documentation]"
		if ($LASTEXITCODE -ne 0) { throw "PALM Tracer installation failed." }
	}
	finally { [Environment]::SetEnvironmentVariable("SETUPTOOLS_SCM_PRETEND_VERSION_FOR_PALM_TRACER", $previousScmVersion, "Process") }
}

function Enable-LongPaths {
	<#
	.SYNOPSIS
		Propose l'activation des chemins Win32 longs.
	#>
	$registryPath = "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem"
	$currentValue = Get-ItemPropertyValue -LiteralPath $registryPath -Name "LongPathsEnabled" -ErrorAction SilentlyContinue
	if ($currentValue -eq 1) {
		Write-Host "Windows long path support is already enabled."
		return
	}

	if (Confirm-Choice "Enable Windows long path support? A restart may be required") {
		New-ItemProperty -LiteralPath $registryPath -Name "LongPathsEnabled" -Value 1 -PropertyType DWord -Force | Out-Null
		Write-Host "Windows long path support has been enabled."
	}
}

if (-not (Test-Administrator)) {
	try {
		Start-ElevatedInstaller
		exit 0
	}
	catch {
		Write-Host "Administrator elevation was cancelled or failed: $($_.Exception.Message)" -ForegroundColor Red
		Write-Host "Please use the step-by-step installation guide: $TutorialUrl"
		Read-Host "Press Enter to close"
		exit 1
	}
}

$transcriptStarted = $false
$exitCode = 0
try {
	try {
		Start-Transcript -LiteralPath $LogPath -Append | Out-Null
		$transcriptStarted = $true
	}
	catch { Write-Host "Warning: the installation log could not be started." -ForegroundColor Yellow }

	Write-Host "PALM Tracer automatic installation" -ForegroundColor Green
	Write-Host "Installation log: $LogPath"

	Show-Step -Number 1 -Message "Checking Python"
	$python = Select-Python
	Write-Host "Selected Python $($python.Version): $($python.Path)"

	Show-Step -Number 2 -Message "Checking Microsoft C++ Build Tools"
	Install-CppBuildTools

	Show-Step -Number 3 -Message "Configuring the Python environment"
	Write-Host "No virtual environment was created because it is not required for the standard PALM Tracer installation."

	Show-Step -Number 4 -Message "Installing PALM Tracer"
	Install-PalmTracer -PythonPath $python.Path

	Show-Step -Number 5 -Message "Creating the desktop shortcut"
	& (Join-Path $ProjectPath "make_shortcut.ps1") -PythonPath $python.Path

	Enable-LongPaths

	Show-Step -Number 6 -Message "Starting PALM Tracer"
	$desktopPath = [Environment]::GetFolderPath([Environment+SpecialFolder]::Desktop)
	$shortcutPath = Join-Path $desktopPath "PALM Tracer.lnk"
	if ($SkipLaunch) { Write-Host "PALM Tracer launch was skipped." }
	else {
		Start-Process -FilePath $shortcutPath
		Write-Host "PALM Tracer is starting. Check that the application opens correctly."
	}

	Write-Host ""
	Write-Host "PALM Tracer installation completed successfully." -ForegroundColor Green
}
catch {
	$exitCode = 1
	Write-Host ""
	Write-Host "Automatic installation failed: $($_.Exception.Message)" -ForegroundColor Red
	Write-Host "Please use the step-by-step installation guide: $TutorialUrl" -ForegroundColor Yellow
	Write-Host "Installation log: $LogPath"
}
finally { if ($transcriptStarted) { Stop-Transcript | Out-Null } }

Read-Host "Press Enter to close this installer"
exit $exitCode
