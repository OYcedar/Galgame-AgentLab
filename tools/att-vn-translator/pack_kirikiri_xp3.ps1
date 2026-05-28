param(
    [string]$SourceDir = "work\patch_src",
    [string]$OutputXp3 = "work\dist\patch_chs.xp3",
    [string]$GarbroDir = "tools\GARbro",
    [string]$Scheme = ""
)

$ErrorActionPreference = "Stop"

$source = [System.IO.Path]::GetFullPath($SourceDir)
$output = [System.IO.Path]::GetFullPath($OutputXp3)
$garbro = [System.IO.Path]::GetFullPath($GarbroDir)

if (-not (Test-Path -LiteralPath $source -PathType Container)) {
    throw "Source directory does not exist: $source"
}
if (-not (Test-Path -LiteralPath $garbro -PathType Container)) {
    throw "GARbro directory does not exist: $garbro"
}

New-Item -ItemType Directory -Force -Path ([System.IO.Path]::GetDirectoryName($output)) | Out-Null

[System.AppDomain]::CurrentDomain.add_AssemblyResolve({
    param($sender, $args)
    $dll = ($args.Name -split ',')[0] + ".dll"
    $path = Join-Path $garbro $dll
    if (Test-Path -LiteralPath $path) {
        return [System.Reflection.Assembly]::LoadFrom($path)
    }
    return $null
})

Add-Type -Path (Join-Path $garbro "GameRes.dll")
Add-Type -Path (Join-Path $garbro "ArcFormats.dll")
Add-Type -Path (Join-Path $garbro "ArcLegacy.dll")
Add-Type -Path (Join-Path $garbro "ArcExtra.dll")

$formats = Join-Path $garbro "GameData\Formats.dat"
if (Test-Path -LiteralPath $formats) {
    $stream = [System.IO.File]::OpenRead($formats)
    try {
        [GameRes.FormatCatalog]::Instance.DeserializeScheme($stream)
    } finally {
        $stream.Dispose()
    }
}

$opener = [GameRes.FormatCatalog]::Instance.ArcFormats | Where-Object { $_.Tag -eq "XP3" } | Select-Object -First 1
if ($null -eq $opener) {
    throw "GARbro XP3 opener was not found"
}
$options = [GameRes.Formats.KiriKiri.Xp3Options]::new()
$options.Version = 2
$options.CompressIndex = $true
$options.CompressContents = $true
$options.RetainDirs = $true

if ([string]::IsNullOrWhiteSpace($Scheme) -or $Scheme.ToLowerInvariant() -eq "none") {
    $options.Scheme = [GameRes.Formats.KiriKiri.NoCrypt]::new()
}
else {
    if ($opener.Scheme.KnownSchemes.ContainsKey($Scheme)) {
        $options.Scheme = $opener.Scheme.KnownSchemes[$Scheme]
    } else {
        $known = ($opener.Scheme.KnownSchemes.Keys | Sort-Object) -join "`n"
        throw "XP3 scheme not found: $Scheme`nKnown schemes:`n$known"
    }
}

$oldLocation = Get-Location
Set-Location -LiteralPath $source
try {
    [GameRes.VFS]::ChDir($source)
    $entries = New-Object "System.Collections.Generic.List[GameRes.Entry]"
    $files = Get-ChildItem -LiteralPath $source -Recurse -File | Sort-Object FullName
    foreach ($file in $files) {
        $rel = $file.FullName.Substring($source.Length).TrimStart("\", "/").Replace("\", "/")
        $entry = [GameRes.Entry]::new()
        $entry.Name = $rel
        $entry.Size = [uint32]$file.Length
        $entry.Offset = 0
        $entry.Type = [GameRes.FormatCatalog]::Instance.GetTypeFromName($rel, [string[]]@())
        $entries.Add($entry)
    }

    if (Test-Path -LiteralPath $output) {
        Remove-Item -LiteralPath $output -Force
    }

    $callback = [GameRes.EntryCallback]{
        param([int]$num, [GameRes.Entry]$entry, [string]$message)
        return [GameRes.ArchiveOperation]::Continue
    }

    $outStream = [System.IO.File]::Create($output)
    try {
        $opener.Create($outStream, $entries, $options, $callback)
    } finally {
        $outStream.Dispose()
    }
} finally {
    Set-Location $oldLocation
}

$info = Get-Item -LiteralPath $output
[pscustomobject]@{
    output = $info.FullName
    bytes = $info.Length
    scheme = $Scheme
    source = $source
} | ConvertTo-Json -Depth 3
