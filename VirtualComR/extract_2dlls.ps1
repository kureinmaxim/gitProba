# Read the input file
$content = Get-Content -Path "dll_list.txt"

# Create arrays to store all DLLs and non-system DLLs
$allDlls = @()
$nonSystemDlls = @()

# Process each line
foreach ($line in $content) {
    if ($line -match "\.dll$") {
        # Extract the file path which is the last part of the line
        $parts = $line.Trim() -split "\s+"
        $path = $parts[-1]
        
        # Extract just the filename
        if ($path -match "([^\\]+\.dll)$") {
            $dllName = $matches[1]
            $allDlls += $dllName
            
            # Check if it's not a system DLL
            if (-not ($path -match "C:\\Windows\\")) {
                $nonSystemDlls += $dllName
            }
        }
    }
}

# Write all DLLs to file
$allDlls | Out-File -FilePath "dll_list_all.txt"

# Write non-system DLLs to file
if ($nonSystemDlls.Count -gt 0) {
    $nonSystemDlls | Out-File -FilePath "dll_list_filtered.txt"
    Write-Host "Found $($nonSystemDlls.Count) non-system DLLs."
} else {
    Write-Host "No non-system DLLs found."
    # Write a note to the filtered file
    "No non-system DLLs found." | Out-File -FilePath "dll_list_filtered.txt"
}

Write-Host "Total DLLs found: $($allDlls.Count)"