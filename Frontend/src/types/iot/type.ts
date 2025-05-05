export interface Sensor {
  id: number;
  nombre: string;
  tipo: string;
  ubicacion: string;
  estado: string;
  tipo_sensor: string;  
  unidad_medida: string;  
  descripcion: string;  
  medida_minima: number;  
  medida_maxima: number;  
}

export interface SensorData {
  id: number;
  sensor: number; 
  temperatura: number;
  humedad: number;
  radiacion_solar: number;
  velocidad_viento: number;
  fecha: string;
  fecha_medicion: string;  
}

export interface EvapotranspiracionData {
  fecha: string;
  et0: number;  
  cultivoId: number;
  bancalId: number;
}