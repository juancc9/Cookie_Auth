import React, { useState, useEffect, useRef } from "react";
import DefaultLayout from "@/layouts/default";
import { motion } from "framer-motion";
import { LineChart, Line, XAxis, YAxis, Tooltip } from "recharts";
import { Droplet, Wind, Sunrise, Sunset, AlertCircle, ChevronLeft, ChevronRight } from "lucide-react";

interface WeatherData {
  coord: { lon: number; lat: number };
  weather: { id: number; main: string; description: string; icon: string }[];
  main: { temp: number; humidity: number };
  wind: { speed: number };
  sys: { sunrise: number; sunset: number };
  dt: number;
  name: string;
}

interface Activity {
  title: string;
  date: string;
  time: string;
}

const Dashboard: React.FC = () => {
  const [weather, setWeather] = useState<WeatherData | null>(null);
  const currentDate = new Date("2025-04-03");
  const scrollContainerRef = useRef<HTMLDivElement>(null);

  const activities: Activity[] = [
    { title: "Riego automático", date: "2025-03-30", time: "06:00 AM" },
    { title: "Revisión de bancales", date: "2025-04-05", time: "10:00 AM" },
    { title: "Fertilización", date: "2025-04-10", time: "08:00 AM" },
    { title: "Cosecha parcial", date: "2025-03-25", time: "09:00 AM" },
  ];

  const pastActivities = activities.filter((activity) => new Date(activity.date) < currentDate);
  const futureActivities = activities.filter((activity) => new Date(activity.date) >= currentDate);

  const notifications = [
    "Recordatorio: Revisar inventario de herramientas esta semana.",
    "Alerta: Posible lluvia fuerte mañana por la tarde.",
  ];

  const salesData = [
    { day: "Sem1", amount: 5000 },
    { day: "Sem2", amount: 6000 },
    { day: "Sem3", amount: 4500 },
    { day: "Sem4", amount: 5500 },
  ];

  useEffect(() => {
    fetch(
      `https://api.openweathermap.org/data/2.5/weather?q=Pitalito&appid=1912de4d8f25e4b41824e3920aed0598&units=metric&lang=es`
    )
      .then((response) => response.json())
      .then((data) => setWeather(data))
      .catch((error) => console.error("Error fetching weather data:", error));
  }, []);

  const scrollLeft = () => {
    if (scrollContainerRef.current) {
      scrollContainerRef.current.scrollBy({ left: -300, behavior: "smooth" });
    }
  };

  const scrollRight = () => {
    if (scrollContainerRef.current) {
      scrollContainerRef.current.scrollBy({ left: 300, behavior: "smooth" });
    }
  };

  const backgroundImage =
    "https://images.unsplash.com/photo-1505576399279-565b52d4ac71?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80&brightness=50";
  const weatherBackgroundImage =
    "https://images.unsplash.com/photo-1506748686214-e9df14d4d9d0?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80&brightness=60";

  return (
    <DefaultLayout>
      <section
        className="flex flex-col items-center gap-6 py-8 px-4 min-h-screen bg-cover bg-center overflow-hidden"
        style={{
          backgroundImage: `url(${backgroundImage}), linear-gradient(to bottom, #e0f7fa, #ffffff)`,
          backgroundSize: "cover",
        }}
      >
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
          className="bg-white/80 backdrop-blur-lg rounded-2xl shadow-2xl p-6 w-full max-w-3xl text-center bg-cover bg-center relative"
          style={{
            backgroundImage: `url(${weatherBackgroundImage}), linear-gradient(to bottom, #f0f4f8, #ffffff)`,
            backgroundSize: "cover",
          }}
        >
          <div className="relative z-10">
            <h1 className="text-2xl sm:text-3xl font-bold font-poppins text-white mb-4">Clima en Pitalito</h1>
            {weather ? (
              <div className="space-y-4">
                <div className="flex justify-center items-center space-x-4 flex-wrap">
                  <img
                    src={`http://openweathermap.org/img/wn/${weather.weather[0].icon}@2x.png`}
                    alt="weather icon"
                    className="w-12 h-12 sm:w-16 sm:h-16"
                    onError={(e) => {
                      (e.target as HTMLImageElement).src = "https://via.placeholder.com/80";
                    }}
                  />
                  <div>
                    <p className="text-3xl sm:text-4xl font-bold text-white">{Math.round(weather.main.temp)}°C</p>
                    <p className="text-base sm:text-lg capitalize text-white">{weather.weather[0].description}</p>
                  </div>
                </div>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 w-full">
                  {/* Ajuste para separar logos con barra vertical */}
                  <div className="flex items-center justify-center space-x-2 text-white">
                    <Droplet className="w-5 h-5 text-blue-600" />
                    <span className="text-sm sm:text-base">{weather.main.humidity}%</span>
                  </div>
                  <div className="flex items-center justify-center space-x-2 text-white relative">
                    <span className="absolute left-[-8px] text-gray-300">|</span>
                    <Wind className="w-5 h-5 text-green-600" />
                    <span className="text-sm sm:text-base">{weather.wind.speed} m/s</span>
                  </div>
                  <div className="flex items-center justify-center space-x-2 text-white relative">
                    <span className="absolute left-[-8px] text-gray-300">|</span>
                    <Sunrise className="w-5 h-5 text-orange-600" />
                    <span className="text-sm sm:text-base">{new Date(weather.sys.sunrise * 1000).toLocaleTimeString()}</span>
                  </div>
                  <div className="flex items-center justify-center space-x-2 text-white relative">
                    <span className="absolute left-[-8px] text-gray-300">|</span>
                    <Sunset className="w-5 h-5 text-purple-600" />
                    <span className="text-sm sm:text-base">{new Date(weather.sys.sunset * 1000).toLocaleTimeString()}</span>
                  </div>
                </div>
              </div>
            ) : (
              <p className="text-gray-500">Cargando...</p>
            )}
          </div>
        </motion.div>

        <div className="relative w-full max-w-5xl mx-auto px-4">
          <button
            onClick={scrollLeft}
            className="absolute left-0 top-1/2 transform -translate-y-1/2 bg-gray-800/50 text-white p-2 rounded-full hover:bg-gray-800 z-10 sm:block hidden"
          >
            <ChevronLeft className="w-6 h-6" />
          </button>

          <div
            ref={scrollContainerRef}
            className="flex flex-row gap-6 py-4 overflow-x-auto no-scrollbar" // Aumenté el gap entre ítems
          >
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="bg-white/70 backdrop-blur-lg rounded-xl shadow-xl p-6 hover:shadow-2xl transition-shadow min-w-[280px] sm:min-w-[300px] flex-shrink-0"
            >
              <h2 className="text-lg sm:text-xl font-semibold text-gray-800 mb-4">Actividades Futuras</h2>
              <ul className="list-disc list-inside text-gray-700 space-y-2 text-sm sm:text-base">
                {futureActivities.slice(0, 3).map((activity, index) => (
                  <li key={index}>
                    {activity.title} - {activity.date}
                  </li>
                ))}
              </ul>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, delay: 0.3 }}
              className="bg-white/70 backdrop-blur-lg rounded-xl shadow-xl p-6 hover:shadow-2xl transition-shadow min-w-[280px] sm:min-w-[300px] flex-shrink-0"
            >
              <h2 className="text-lg sm:text-xl font-semibold text-gray-800 mb-4">Actividades Vencidas</h2>
              <ul className="list-disc list-inside text-gray-700 space-y-2 text-sm sm:text-base">
                {pastActivities.slice(0, 3).map((activity, index) => (
                  <li key={index}>
                    {activity.title} - {activity.date}
                  </li>
                ))}
              </ul>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, delay: 0.4 }}
              className="bg-white/70 backdrop-blur-lg rounded-xl shadow-xl p-6 hover:shadow-2xl transition-shadow min-w-[280px] sm:min-w-[300px] flex-shrink-0"
            >
              <h2 className="text-lg sm:text-xl font-semibold text-gray-800 mb-4">Ganancias del Mes</h2>
              <LineChart width={260} height={150} data={salesData}>
                <XAxis dataKey="day" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="amount" stroke="#10B981" />
              </LineChart>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, delay: 0.5 }}
              className="bg-white/70 backdrop-blur-lg rounded-xl shadow-xl p-6 hover:shadow-2xl transition-shadow min-w-[280px] sm:min-w-[300px] flex-shrink-0"
            >
              <h2 className="text-lg sm:text-xl font-semibold text-gray-800 mb-4">Notificaciones</h2>
              <ul className="list-none text-gray-700 space-y-2 text-sm sm:text-base">
                {notifications.map((notification, index) => (
                  <li key={index} className="flex items-center space-x-2">
                    <AlertCircle className="w-5 h-5 text-blue-500" />
                    <p>{notification}</p>
                  </li>
                ))}
              </ul>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, delay: 0.6 }}
              className="bg-white/70 backdrop-blur-lg rounded-xl shadow-xl p-6 hover:shadow-2xl transition-shadow min-w-[280px] sm:min-w-[300px] flex-shrink-0"
            >
              <h2 className="text-lg sm:text-xl font-semibold text-gray-800 mb-4">Estadísticas</h2>
              <div className="space-y-2 text-gray-700 text-sm sm:text-base">
                <p><strong>Cultivos Activos:</strong> 5</p>
                <p><strong>Tareas Pendientes:</strong> 3</p>
              </div>
            </motion.div>
          </div>

          <button
            onClick={scrollRight}
            className="absolute right-0 top-1/2 transform -translate-y-1/2 bg-gray-800/50 text-white p-2 rounded-full hover:bg-gray-800 z-10 sm:block hidden"
          >
            <ChevronRight className="w-6 h-6" />
          </button>
        </div>
      </section>

      <style>{`
        .no-scrollbar {
          -ms-overflow-style: none; /* Oculta scrollbar en IE y Edge */
          scrollbar-width: none; /* Oculta scrollbar en Firefox */
          overflow-x: auto;
          overflow-y: hidden; /* Evita scroll vertical */
        }
        .no-scrollbar::-webkit-scrollbar {
          display: none; /* Oculta scrollbar en Chrome, Safari */
        }
        section {
          overflow-y: hidden;
        }
        @media (max-width: 640px) {
          .no-scrollbar {
            padding-left: 0;
            padding-right: 0;
          }
          .min-w-[280px] {
            min-width: calc(100% - 2rem); /* Ocupa casi todo el ancho en móviles */
          }
        }
        @media (min-width: 640px) {
          .no-scrollbar {
            gap: 1.5rem; /* Aumenté el gap entre ítems para pantallas grandes */
          }
        }
      `}</style>
    </DefaultLayout>
  );
};

export default Dashboard;