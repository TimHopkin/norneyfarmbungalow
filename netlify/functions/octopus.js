// Proxy for Octopus Energy API
// Handles: /octopus/* → https://api.octopus.energy/v1/*
export default async (req, context) => {
  const url = new URL(req.url);
  const path = url.pathname.replace('/.netlify/functions/octopus', '').replace('/octopus', '');
  const octopusUrl = `https://api.octopus.energy/v1${path}${url.search}`;

  const auth = Buffer.from(`${process.env.OCTOPUS_KEY}:`).toString('base64');

  const resp = await fetch(octopusUrl, {
    headers: {
      'Authorization': `Basic ${auth}`,
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

export const config = { path: '/octopus/*' };
