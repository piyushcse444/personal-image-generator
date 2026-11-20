 Get-ChildItem .\videos -File | ForEach-Object {
>>     $name = [IO.Path]::GetFileNameWithoutExtension($_.Name)
>>     New-Item -ItemType Directory -Force ".\frames\$name" | Out-Null
>>     ffmpeg -i $_.FullName -vf "fps=1" ".\frames\$name\frame_%05d.png"
>> }