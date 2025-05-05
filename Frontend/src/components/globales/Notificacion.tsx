import React, { useEffect, useState } from "react";
import { useAuth } from "@/context/AuthContext";
import { IconButton, Badge, Menu, MenuItem, Typography, Box } from "@mui/material";
import NotificationsIcon from "@mui/icons-material/Notifications";

interface Notification {
  id: string;
  type: string;
  message: string;
  actividad: {
    id: number;
    tipo_actividad_nombre: string;
    prioridad: string;
    descripcion: string;
  };
  timestamp: string;
}

const Notificacion: React.FC = () => {
  const { user } = useAuth();
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);
  const wsRef = React.useRef<WebSocket | null>(null);

  useEffect(() => {
    if (!user?.id) return;

    const socketUrl = `ws://${window.location.hostname}:8000/ws/actividades/notificaciones/${user.id}/`;
    wsRef.current = new WebSocket(socketUrl);

    wsRef.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log('Notificación recibida:', data);

        const newNotification: Notification = {
          id: `notif-${Date.now()}-${data.actividad.id}`,
          type: data.type,
          message: data.message,
          actividad: {
            id: data.actividad.id,
            tipo_actividad_nombre: data.actividad.tipo_actividad_nombre,
            prioridad: data.actividad.prioridad,
            descripcion: data.actividad.descripcion
          },
          timestamp: new Date().toISOString()
        };

        setNotifications(prev => [newNotification, ...prev]);
        setUnreadCount(prev => open ? prev : prev + 1);

     

      } catch (error) {
        console.error('Error procesando notificación:', error);
      }
    };

    return () => {
      if (wsRef.current?.readyState === WebSocket.OPEN) {
        wsRef.current.close();
      }
    };
  }, [user?.id, open]);

  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
    setUnreadCount(0);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <Box sx={{ display: 'flex', alignItems: 'center', mr: 2 }}>
      <IconButton
        onClick={handleClick}
        sx={{ color: '#fff' }}
        aria-label="notificaciones"
      >
        <Badge badgeContent={unreadCount} color="error">
          <NotificationsIcon sx={{ color: '#fff' }} />
        </Badge>
      </IconButton>

      <Menu
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
        transformOrigin={{ vertical: 'top', horizontal: 'right' }}
        PaperProps={{
          sx: {
            width: 350,
            maxHeight: 400,
            overflow: 'auto',
            mt: 1
          }
        }}
      >
        {notifications.length === 0 ? (
          <MenuItem dense>
            <Typography variant="body2">No hay notificaciones</Typography>
          </MenuItem>
        ) : (
          notifications.map((notification) => (
            <MenuItem 
              key={notification.id} 
              dense
              onClick={handleClose}
              sx={{
                borderBottom: '1px solid rgba(0, 0, 0, 0.12)',
                '&:last-child': { borderBottom: 'none' }
              }}
            >
              <Box sx={{ py: 1, width: '100%' }}>
                <Typography variant="subtitle2" fontWeight="bold">
                  {notification.message}
                </Typography>
                <Typography variant="body2">
                  <strong>Tipo:</strong> {notification.actividad.tipo_actividad_nombre}
                </Typography>
                <Typography variant="body2">
                  <strong>Prioridad:</strong> {notification.actividad.prioridad}
                </Typography>
                {notification.actividad.descripcion && (
                  <Typography variant="body2" sx={{ mt: 1 }}>
                    {notification.actividad.descripcion}
                  </Typography>
                )}
              </Box>
            </MenuItem>
          ))
        )}
      </Menu>
    </Box>
  );
};

export default Notificacion;