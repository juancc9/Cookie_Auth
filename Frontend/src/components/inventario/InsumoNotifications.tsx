import React, { useEffect, useState, useRef } from "react";
import { addToast } from "@heroui/toast";

interface Notification {
  message: string;
  type: "info" | "warning" | "alert" | "error";
  timestamp: number;
  insumoId?: number;
  uniqueId?: string;
}

interface InsumoNotificationsProps {
  userId1: number;
  isAdmin?: boolean;
}

const InsumoNotifications: React.FC<InsumoNotificationsProps> = ({ 
  userId1, 
  isAdmin = false 
}) => {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const socketRef = useRef<WebSocket | null>(null);
  const receivedIds = useRef<Set<string>>(new Set());
  const reconnectTimer = useRef<NodeJS.Timeout | null>(null);

  const connectWebSocket = () => {
    if ((!userId1 || userId1 === 0) && !isAdmin) return;

    const wsUrl = isAdmin 
      ? `ws://${window.location.hostname}:8000/ws/insumo/admin/` 
      : `ws://${window.location.hostname}:8000/ws/insumo/${userId1}/`;

    console.log(`Conectando a WebSocket: ${wsUrl}`);
    socketRef.current = new WebSocket(wsUrl);

    socketRef.current.onopen = () => {
      console.log("Conexión WebSocket de insumos establecida correctamente");
      if (reconnectTimer.current) {
        clearTimeout(reconnectTimer.current);
        reconnectTimer.current = null;
      }
    };

    socketRef.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log("Mensaje recibido:", data);
        
        if (data.hash && receivedIds.current.has(data.hash)) {
          console.log("Notificación duplicada ignorada:", data.hash);
          return;
        }

        if (data.hash) {
          receivedIds.current.add(data.hash);
        }

        const newNotification: Notification = {
          message: data.message,
          type: data.notification_type || "info",
          timestamp: data.timestamp || Date.now(),
          insumoId: data.insumo_id,
          uniqueId: data.hash
        };

        setNotifications(prev => {
          const isDuplicate = prev.some(
            n => n.message === data.message && 
                 n.timestamp === newNotification.timestamp
          );
          return isDuplicate ? prev : [newNotification, ...prev.slice(0, 19)];
        });

        addToast({
          title: "Estado de Insumo",
          description: data.message,
          timeout: 60000,  // 60 segundos
        });
      } catch (error) {
        console.error("Error procesando mensaje de insumos:", error);
      }
    };

    socketRef.current.onerror = (error) => {
      console.error("Error en WebSocket de insumos:", error);
    };

    socketRef.current.onclose = (event) => {
      console.log(`WebSocket cerrado. Código: ${event.code}, Razón: ${event.reason}`);
      if (!reconnectTimer.current) {
        reconnectTimer.current = setTimeout(() => {
          console.log("Reconectando WebSocket...");
          connectWebSocket();
        }, 3000);
      }
    };
  };

  useEffect(() => {
    connectWebSocket();

    // Temporizador para eliminar notificaciones después de 60 segundos
    const interval = setInterval(() => {
      setNotifications(prev => {
        const now = Date.now();
        return prev.filter(notif => now - Number(notif.timestamp) < 60000); // 60 segundos
      });
    }, 1000); // Verificar cada segundo

    return () => {
      if (socketRef.current) {
        socketRef.current.close();
      }
      if (reconnectTimer.current) {
        clearTimeout(reconnectTimer.current);
      }
      clearInterval(interval); // Limpiar el temporizador
    };
  }, [userId1, isAdmin]);

  return (
    <div className="fixed bottom-4 right-4 w-80 bg-white p-4 rounded-lg shadow-lg border border-gray-200 z-50">
      <h2 className="text-lg font-semibold mb-2">Notificaciones de Insumos</h2>
      <div className="max-h-60 overflow-y-auto">
        {notifications.length === 0 ? (
          <p className="text-gray-500 text-sm">No hay notificaciones recientes</p>
        ) : (
          notifications.map((notif, index) => (
            <div key={`${notif.uniqueId || index}`} className="mb-2 pb-2 border-b border-gray-100">
              <p className={`text-sm ${
                notif.type === "error" ? "text-red-600" :
                notif.type === "warning" ? "text-yellow-600" :
                notif.type === "alert" ? "text-orange-600" : 
                "text-green-600"
              }`}>
                {notif.message}
              </p>
              <p className="text-xs text-gray-400">
                {new Date(notif.timestamp).toLocaleTimeString()}
              </p>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default InsumoNotifications;