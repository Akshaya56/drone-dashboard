let altitudeChart = null;
let altitudeData = {
  labels: [],
  datasets: [{
    label: 'Altitude (m)',
    data: [],
    backgroundColor: 'rgba(59, 130, 246, 0.2)',
    borderColor: 'rgba(59, 130, 246, 1)',
    borderWidth: 2,
    fill: true,
    tension: 0.3
  }]
};

// Chart setup
window.onload = function () {
  const ctx = document.getElementById('altitudeChart').getContext('2d');
  altitudeChart = new Chart(ctx, {
    type: 'line',
    data: altitudeData,
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });

  updateTelemetry();
  setInterval(updateTelemetry, 1000);
};

function updateTelemetry() {
  fetch('/telemetry')
    .then(response => response.json())
    .then(data => {
      document.getElementById('battery_voltage').textContent = `${data.battery_voltage} V`;
      document.getElementById('imu_data').textContent = `Roll: ${data.imu.roll}° | Pitch: ${data.imu.pitch}° | Yaw: ${data.imu.yaw}°`;
      document.getElementById('temperature').textContent = `${data.temperature} °C`;
      document.getElementById('altitude').textContent = `${data.altitude} m`;
      document.getElementById('connection_health').textContent = data.connection_health;
      document.getElementById('gps').textContent = `Lat: ${data.gps.split(',')[0]} | Lon: ${data.gps.split(',')[1]} | Alt: ${data.altitude} m`;

      // Update Chart
      const now = new Date().toLocaleTimeString();
      if (altitudeData.labels.length > 20) {
        altitudeData.labels.shift();
        altitudeData.datasets[0].data.shift();
      }
      altitudeData.labels.push(now);
      altitudeData.datasets[0].data.push(data.altitude);
      altitudeChart.update();

      // Update GPS map
      const coords = data.gps.split(',');
      const lat = parseFloat(coords[0]);
      const lon = parseFloat(coords[1]);
      updateMap(lat, lon);
    });
}
