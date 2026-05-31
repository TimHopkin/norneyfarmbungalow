// Proxy for Victron VRM API
// Handles: /api/* → https://vrmapi.victronenergy.com/v2/*
export default async (req, context) => {
  const url = new URL(req.url);
  // Strip the /.netlify/functions/api prefix to get the VRM path
  const path = url.pathname.replace('/.netlify/functions/api', '').replace('/api', '');
  const vrm = `https://vrmapi.victronenergy.com/v2${path}${url.search}`;

  const resp = await fetch(vrm, {
    headers: {
      'x-authorization': `Token ${process.env.VICTRON_KEY}`,
      'Content-Type': 'application/json',
    },
  });

  const body = await resp.text();
  return new Response(body, {
    status: resp.status,
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
    },
  });
};

export const config = { path: '/api/*' };
