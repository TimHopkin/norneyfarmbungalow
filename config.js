// Tunnel URL is set here — update after running: cloudflared tunnel route dns norney <tunnel-id>
const TUNNEL_URL = 'https://cited-motion-hampton-ohio.trycloudflare.com';

// Automatically use local proxy when running on localhost, tunnel URL when deployed
const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
const PROXY_BASE = isLocal ? '' : TUNNEL_URL;
