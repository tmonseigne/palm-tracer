Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Get-PalmTracerPythonPath {
	<#
	.SYNOPSIS
		Retourne l'interpréteur Python à utiliser pour lancer PALM Tracer.
	#>
	$virtualEnvironmentPythonPath = Join-Path $PSScriptRoot "venv\Scripts\python.exe"
	if (Test-Path -LiteralPath $virtualEnvironmentPythonPath -PathType Leaf) {
		return (Resolve-Path -LiteralPath $virtualEnvironmentPythonPath).Path
	}

	$pythonCommand = Get-Command python.exe -CommandType Application -All -ErrorAction Stop |
		Select-Object -First 1
	return $pythonCommand.Source
}

try {
	$pythonPath = Get-PalmTracerPythonPath
	& $pythonPath -c "import importlib.util, sys; sys.exit(0 if importlib.util.find_spec('napari') and importlib.util.find_spec('palm_tracer') else 1)"
	if ($LASTEXITCODE -ne 0) {
		throw "Napari ou PALM Tracer n'est pas accessible avec l'interpréteur '$pythonPath'."
	}

	$desktopPath = [Environment]::GetFolderPath([Environment+SpecialFolder]::Desktop)
	if ([string]::IsNullOrWhiteSpace($desktopPath)) {
		throw "Le dossier du bureau Windows est introuvable."
	}

	$powerShellPath = (Get-Command powershell.exe -CommandType Application -ErrorAction Stop).Source
	$shortcutPath = Join-Path $desktopPath "PALM Tracer.lnk"
	$escapedPythonPath = $pythonPath.Replace("'", "''")
	$command = "& '$escapedPythonPath' -m napari -w palm-tracer"

	$shell = New-Object -ComObject WScript.Shell
	$shortcut = $shell.CreateShortcut($shortcutPath)
	$shortcut.TargetPath = $powerShellPath
	$shortcut.Arguments = "-NoProfile -Command `"$command`""
	$shortcut.WorkingDirectory = $PSScriptRoot

	$iconPath = Join-Path $PSScriptRoot "docs\_static\favicon.ico"
	if (Test-Path -LiteralPath $iconPath -PathType Leaf) {
		$shortcut.IconLocation = "$iconPath,0"
	}

	$shortcut.Save()
	Write-Host "Le raccourci '$shortcutPath' a été créé avec succès."
}
catch {
	Write-Error $_
	exit 1
}
