fetch('/zones')
  .then(res => res.json())
  .then(zones => {
    document.body.style.backgroundColor = "white";

    let html = "<h2>Taxi Zones</h2><ul>";
    zones.slice(0, 20).forEach(z => {
      html += `<li>${z.Zone} (${z.Borough})</li>`;
    });
    html += "</ul>";

    document.getElementById("zones-map").innerHTML = html;
  })
  .catch(err => {
    document.body.innerHTML = "<h1>Error loading zones</h1>";
    console.error(err);
  });
