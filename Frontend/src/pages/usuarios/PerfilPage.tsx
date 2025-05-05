import React, { useState, FormEvent } from "react";
import { useAuth } from "@/context/AuthContext";
import { useUsuarios, UsuarioUpdate } from "@/hooks/usuarios/useUsuarios";
import DefaultLayout from "@/layouts/default";
import {
  Box,
  Button,
  TextField,
  Typography,
  Modal,
  Backdrop,
  Fade,
  IconButton,
  InputAdornment,
} from "@mui/material";
import { motion } from "framer-motion";
import api from "@/components/utils/axios";
import { toast } from "react-hot-toast";
import Visibility from "@mui/icons-material/Visibility";
import VisibilityOff from "@mui/icons-material/VisibilityOff";

const PerfilPage: React.FC = () => {
  const { user, updateUser, token, logout } = useAuth();
  const { updateUsuario } = useUsuarios();
  const [isEditing, setIsEditing] = useState(false);
  const [editUser, setEditUser] = useState(user);
  const [editError, setEditError] = useState<string | null>(null);
  const [openModal, setOpenModal] = useState(false);
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmNewPassword, setConfirmNewPassword] = useState("");
  const [passwordError, setPasswordError] = useState<string | null>(null);
  const [showCurrentPassword, setShowCurrentPassword] = useState(false);
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const textFieldStyles = {
    '& .MuiOutlinedInput-root': {
      borderRadius: '12px',
      backgroundColor: '#fff',
      transition: 'all 0.3s ease-in-out',
      '& fieldset': { borderColor: '#e2e8f0' },
      '&:hover fieldset': { borderColor: '#cbd5e1' },
      '&.Mui-focused fieldset': { borderColor: '#2ecc71' },
      '&.Mui-disabled': { backgroundColor: '#fff' },
      '& .MuiInputAdornment-root': { backgroundColor: 'inherit', height: '100%' },
    },
    '& .MuiInputLabel-root': {
      color: '#a0aec0',
      '&.Mui-focused': { color: '#2ecc71' },
      '&.Mui-disabled': { color: '#718096' },
    },
  };

  if (!user || !editUser) {
    return (
      <DefaultLayout>
        <Typography variant="h6" sx={{ textAlign: "center", mt: 4 }}>
          No se encontró información del usuario. Por favor, inicia sesión.
        </Typography>
      </DefaultLayout>
    );
  }

  const handleEdit = () => {
    setIsEditing(true);
    setEditError(null);
    setPasswordError(null);
  };

  const handleCancel = () => {
    setIsEditing(false);
    setEditUser(user);
    setOpenModal(false);
    setCurrentPassword("");
    setNewPassword("");
    setConfirmNewPassword("");
    setEditError(null);
    setPasswordError(null);
    setShowCurrentPassword(false);
    setShowNewPassword(false);
    setShowConfirmPassword(false);
  };

  const handleChange = (field: keyof UsuarioUpdate, value: string) => {
    setEditUser((prev) => prev ? { ...prev, [field]: value } : prev);
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      const usuarioToUpdate: UsuarioUpdate = {
        id: editUser.id,
        nombre: editUser.nombre,
        apellido: editUser.apellido,
        email: editUser.email,
        username: editUser.username,
        rol_id: editUser.rol?.id || null,
      };
      const updatedUser = await updateUsuario(usuarioToUpdate);
      updateUser(updatedUser);
      setIsEditing(false);
      setEditError(null);
      toast.success("Perfil actualizado con éxito.");
    } catch (err: any) {
      setEditError(err.response?.data?.detail || "No se pudo actualizar los datos.");
    }
  };

  const handlePasswordChange = async (e: FormEvent) => {
    e.preventDefault();
    if (newPassword !== confirmNewPassword) {
      setPasswordError("Las nuevas contraseñas no coinciden.");
      return;
    }
    try {
      await api.post(
        "http://127.0.0.1:8000/usuarios/change_password/",
        { current_password: currentPassword, new_password: newPassword },
        { headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" } }
      );
      toast.success("Contraseña actualizada con éxito.");
      logout();
      toast("Debes iniciar sesión de nuevo con tu nueva contraseña.");
    } catch (err: any) {
      setPasswordError(err.response?.data?.error || "Error al cambiar la contraseña.");
    }
  };

  return (
    <DefaultLayout>
      <Box sx={{ p: 4, maxWidth: "600px", mx: "auto" }}>
        <Typography variant="h4" sx={{ mb: 4, textAlign: "center" }}>
          Mi Perfil
        </Typography>
        {!isEditing ? (
          <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
            <TextField label="Nombre" value={user.nombre} disabled fullWidth sx={textFieldStyles} />
            <TextField label="Apellido" value={user.apellido} disabled fullWidth sx={textFieldStyles} />
            <TextField label="Email" value={user.email} disabled fullWidth sx={textFieldStyles} />
            <TextField label="Username" value={user.username || ""} disabled fullWidth sx={textFieldStyles} />
            <TextField label="Rol" value={user.rol?.rol || "Sin rol"} disabled fullWidth sx={textFieldStyles} />
            <TextField label="Contraseña" value="••••••••" disabled fullWidth sx={textFieldStyles} />
            <Box sx={{ display: "flex", justifyContent: "center", mt: 2 }}>
              <Button variant="contained" sx={{ backgroundColor: "#2ecc71" }} onClick={handleEdit}>
                Editar
              </Button>
            </Box>
          </Box>
        ) : (
          <Box component="form" onSubmit={handleSubmit} sx={{ display: "flex", flexDirection: "column", gap: 2.5 }}>
            {editError && (
              <Typography variant="body2" sx={{ color: "#f56565", textAlign: "center" }}>
                {editError}
              </Typography>
            )}
            {/* Aquí puedes seguir con los campos editables, el botón de cambiar contraseña, el modal, etc. */}
          </Box>
        )}
      </Box>
    </DefaultLayout>
  );
};

export default PerfilPage;
