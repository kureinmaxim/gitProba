# Read the input file
$content = Get-Content -Path "dll_list.txt"

# Write entire file content for debugging
$content | Out-File -FilePath "debug_full_content.txt"

# Create a simple extraction of everything that contains .dll
$simpleExtract = $content | Where-Object { $_ -match "\.dll" }
$simpleExtract | Out-File -FilePath "debug_simple_extract.txt"

# Try to extract the last column which should be the path
$pathsOnly = @()
foreach ($line in $content) {
    if ($line -match "\.dll") {
        $parts = $line.Trim() -split "\s+"
        $pathsOnly += $parts[-1]
    }
}
$pathsOnly | Out-File -FilePath "debug_paths_only.txt"

# Extract just the filenames
$filenamesOnly = @()
foreach ($path in $pathsOnly) {
    if ($path -match "([^\\]+\.dll)$") {
        $filenamesOnly += $matches[1]
    }
}
$filenamesOnly | Out-File -FilePath "dll_list_all_filenames.txt"

Write-Host "Debugging complete. Check the debug files to see what's happening."