cd "C:\Users\sneha\snehassneha4578-collab"

$readme = Get-Content README.md -Raw

$start = $readme.IndexOf('<h2 align="center">ENGINEERING FOCUS</h2>')
$end = $readme.IndexOf('</div>', $start)

if ($start -ge 0 -and $end -gt $start) {

    $newSection = @'
<h2 align="center">ENGINEERING FOCUS</h2>

<table>
<tr>
<td align="center" width="25%" valign="top">

<h3>AI / ML</h3>

Computer Vision<br>
TensorFlow<br>
Scikit-learn<br>
Pandas

</td>

<td align="center" width="25%" valign="top">

<h3>EMBEDDED</h3>

ESP32<br>
IoT<br>
Embedded Systems<br>
Hardware Integration

</td>

<td align="center" width="25%" valign="top">

<h3>VLSI</h3>

Verilog HDL<br>
RTL Design<br>
Digital Design<br>
Cadence Virtuoso

</td>

<td align="center" width="25%" valign="top">

<h3>SOFTWARE</h3>

C / C++<br>
Python<br>
Java<br>
JavaScript

</td>
</tr>
</table>

'@

    $readme = $readme.Substring(0, $start) + $newSection + $readme.Substring($end)

    Set-Content README.md $readme -Encoding UTF8

    git add README.md
    git -c core.editor=true commit -m "docs: fix engineering focus column alignment"
    git push origin main

    Write-Host "`nSUCCESS: Engineering Focus alignment fixed." -ForegroundColor Green
}
else {
    Write-Host "`nERROR: Engineering Focus section not found." -ForegroundColor Red
}

Write-Host "`nVERIFYING:`n" -ForegroundColor Cyan
Get-Content README.md | Select-Object -Skip 9 -First 60

Write-Host "`nGIT STATUS:`n" -ForegroundColor Cyan
git status
