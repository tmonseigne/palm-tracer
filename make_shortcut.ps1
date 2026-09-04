param(
	[string]$PythonPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

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

	if ([string]::IsNullOrWhiteSpace($Path) -or $Path -like "*\Microsoft\WindowsApps\*") { return }
	if (Test-Path -LiteralPath $Path -PathType Leaf) { [void]$Paths.Add([IO.Path]::GetFullPath($Path)) }
}

function Get-PalmTracerPythonPath {
	<#
	.SYNOPSIS
		Retourne l'interpréteur Python à utiliser pour lancer PALM Tracer.
	#>
	if (-not [string]::IsNullOrWhiteSpace($PythonPath)) {
		if (-not (Test-Path -LiteralPath $PythonPath -PathType Leaf)) { throw "The requested Python interpreter does not exist: $PythonPath" }
		return (Resolve-Path -LiteralPath $PythonPath).Path
	}

	$virtualEnvironmentPythonPath = Join-Path $PSScriptRoot "venv\Scripts\python.exe"
	if (Test-Path -LiteralPath $virtualEnvironmentPythonPath -PathType Leaf) { return (Resolve-Path -LiteralPath $virtualEnvironmentPythonPath).Path }

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

	$candidates = foreach ($path in $paths) {
		try {
			$versionText = & $path -c "import sys; print('.'.join(map(str, sys.version_info[:3])))" 2>$null
			if ($LASTEXITCODE -eq 0 -and -not [string]::IsNullOrWhiteSpace($versionText)) {
				[pscustomobject]@{
					Path = $path
					Version = [version]$versionText.Trim()
				}
			}
		}
		catch { } # Les alias invalides et installations incomplètes sont ignorés.
	}

	$candidate = $candidates | Sort-Object Version -Descending | Select-Object -First 1
	if ($null -eq $candidate) { throw "No usable Python installation was found." }
	return $candidate.Path
}

try {
	$selectedPythonPath = Get-PalmTracerPythonPath
	& $selectedPythonPath -c "import importlib.util, sys; sys.exit(0 if importlib.util.find_spec('napari') and importlib.util.find_spec('palm_tracer') else 1)"
	if ($LASTEXITCODE -ne 0) { throw "Napari or PALM Tracer is not available with '$selectedPythonPath'." }

	$desktopPath = [Environment]::GetFolderPath([Environment+SpecialFolder]::Desktop)
	if ([string]::IsNullOrWhiteSpace($desktopPath)) { throw "The Windows desktop folder could not be found." }

	$powerShellPath = (Get-Command powershell.exe -CommandType Application -ErrorAction Stop).Source
	$shortcutPath = Join-Path $desktopPath "PALM Tracer.lnk"
	$escapedPythonPath = $selectedPythonPath.Replace("'", "''")
	$command = "& '$escapedPythonPath' -m napari -w palm-tracer"

	$shell = New-Object -ComObject WScript.Shell
	$shortcut = $shell.CreateShortcut($shortcutPath)
	$shortcut.TargetPath = $powerShellPath
	$shortcut.Arguments = "-NoProfile -Command `"$command`""
	$shortcut.WorkingDirectory = $PSScriptRoot

	$iconPath = Join-Path $PSScriptRoot "docs\_static\favicon.ico"
	if (Test-Path -LiteralPath $iconPath -PathType Leaf) { $shortcut.IconLocation = "$iconPath,0" }

	$shortcut.Save()
	Write-Host "The shortcut '$shortcutPath' was created successfully."
}
catch { throw "Failed to create the PALM Tracer shortcut: $($_.Exception.Message)" }
