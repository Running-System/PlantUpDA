Add-Type -AssemblyName System.Drawing
$src = (Resolve-Path 'images\Fogg-Behavior-Model.png').Path
$dst = Join-Path (Split-Path $src) 'Fogg-Behavior-Model-fixed.png'
$img = [System.Drawing.Image]::FromFile($src)
$img.Save($dst, [System.Drawing.Imaging.ImageFormat]::Png)
$img.Dispose()
Remove-Item $src
Rename-Item $dst 'Fogg-Behavior-Model.png'
Write-Host 'PNG re-encoded successfully'
