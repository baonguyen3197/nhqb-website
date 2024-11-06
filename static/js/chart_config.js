document.addEventListener("DOMContentLoaded", function () {
  const weatherDataElement = document.getElementById('weather-data');

  if (!weatherDataElement) {
    console.error("Error: Weather data element is missing.");
    return;
  }

  try {
    const weatherData = JSON.parse(weatherDataElement.textContent);

    console.log("Parsed Weather Data:", weatherData); // Debugging: Log the parsed data

    // Line chart data
    const lineChartOptions = {
      chart: {
        height: 400,
        type: "line",
        fontFamily: "Inter, sans-serif",
        dropShadow: {
          enabled: false,
        },
        toolbar: {
          show: false,
        },
      },
      series: [
        {
          name: "Max Temperature",
          data: weatherData.temperature_2m_max.map(Number),
          color: "#FF5733",
        },
        {
          name: "Min Temperature",
          data: weatherData.temperature_2m_min.map(Number),
          color: "#33A4FF",
        },
        {
          name: "Apparent Max Temperature",
          data: weatherData.apparent_temperature_max.map(Number),
          color: "#FF8C00",
        },
        {
          name: "Apparent Min Temperature",
          data: weatherData.apparent_temperature_min.map(Number),
          color: "#1E90FF",
        },
        {
          name: "UV Index Max",
          data: weatherData.uv_index_max.map(Number),
          color: "#FFD700",
        },
        {
          name: "UV Index Clear Sky Max",
          data: weatherData.uv_index_clear_sky_max.map(Number),
          color: "#FF4500",
        },
      ],
      xaxis: {
        categories: weatherData.date,
        labels: {
          show: true,
          style: {
            fontFamily: "Inter, sans-serif",
            cssClass: 'text-xs font-normal fill-gray-500 dark:fill-gray-400'
          }
        },
      },
      yaxis: {
        title: {
          text: "Values",
        },
      },
    };

    if (document.getElementById("line-chart") && typeof ApexCharts !== 'undefined') {
      const lineChart = new ApexCharts(document.getElementById("line-chart"), lineChartOptions);
      lineChart.render();
    }

    // Column chart data
    const columnChartOptions = {
      chart: {
        height: 400,
        type: 'bar',
        fontFamily: 'Inter, sans-serif',
        dropShadow: {
          enabled: false,
        },
        toolbar: {
          show: false,
        },
      },
      series: [
        {
          name: 'Precipitation Sum',
          data: weatherData.precipitation_sum.map(Number),
          color: '#1E90FF',
        },
        {
          name: 'Rain Sum',
          data: weatherData.rain_sum.map(Number),
          color: '#00BFFF',
        },
        {
          name: 'Showers Sum',
          data: weatherData.showers_sum.map(Number),
          color: '#87CEFA',
        },
        {
          name: 'Snowfall Sum',
          data: weatherData.snowfall_sum.map(Number),
          color: '#B0E0E6',
        },
        {
          name: 'Precipitation Hours',
          data: weatherData.precipitation_hours.map(Number),
          color: '#4682B4',
        },
        {
          name: 'Precipitation Probability Max',
          data: weatherData.precipitation_probability_max.map(Number),
          color: '#5F9EA0',
        },
        {
          name: 'Daylight Duration',
          data: weatherData.daylight_duration.map(Number),
          color: '#FFD700',
        },
        {
          name: 'Sunshine Duration',
          data: weatherData.sunshine_duration.map(Number),
          color: '#FFA500',
        },
      ],
      xaxis: {
        categories: weatherData.date,
        labels: {
          show: true,
          style: {
            fontFamily: 'Inter, sans-serif',
            cssClass: 'text-xs font-normal fill-gray-500 dark:fill-gray-400'
          }
        },
      },
      yaxis: {
        title: {
          text: 'Values',
        },
      },
    };

    if (document.getElementById("column-chart") && typeof ApexCharts !== 'undefined') {
      const columnChart = new ApexCharts(document.getElementById("column-chart"), columnChartOptions);
      columnChart.render();
    }
  } catch (error) {
    console.error("Error parsing JSON data:", error);
    console.log("Error details:", error.message); // Log the error message to the console
  }
});