import React, { useEffect } from "react";
import './../../assets/styles/components/layout/Weather.css';

const Weather = () => {
  useEffect(() => {
    const widgetContainer = document.getElementById("weather-widget-container");

    if (!widgetContainer) return;

    const script = document.createElement("script");
    script.type = "text/javascript";
    script.src = "https://www.eltiempo.es/widget/widget_loader/9cd153d1fe641cda009ad9a3b77ed560";
    script.async = true;

    const widgetDiv = document.createElement("div");
    widgetDiv.id = "c_9cd153d1fe641cda009ad9a3b77ed560";
    widgetDiv.className = "ancho";

    widgetContainer.appendChild(widgetDiv);
    widgetContainer.appendChild(script);

    return () => {
      widgetContainer.innerHTML = "";
    };
  }, []);

  return (
    <>
      <hr className="separator" />
      <div className="weather-all">
        <h2>El tiempo atmosférico en Villanueva de la Cruces en tiempo real:</h2>
        <p>Para que puedas comprobarlo antes de ir y así evitar sorpresas.</p>
        <div id="weather-widget-container"></div>
    </div>
    </>
  );
};

export default Weather;
