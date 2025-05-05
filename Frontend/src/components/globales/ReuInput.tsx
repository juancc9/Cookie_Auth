import React from "react";
import { Input } from "@heroui/react";

interface ReusableInputProps {
  label?: string;
  placeholder?: string;
  type: string;
  variant?: "flat" | "bordered" | "underlined" | "faded";
  radius?: "full" | "lg" | "md" | "sm" | "none";
  value: string | number;
  step?: string;
  min?: number;  
  max?:number;
  onChange: (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => void;
}

export const ReuInput: React.FC<ReusableInputProps> = ({
  label,
  placeholder,
  type,
  variant = "bordered",
  radius = "md",
  value,
  step,
  onChange,
}) => {
  return (
    <div className="w-full">
      <Input
        label={label}
        type={type}
        placeholder={placeholder}
        variant={variant}
        radius={radius}
        value={value.toString()}
        onChange={onChange}
        step={step}
      />
    </div>
  );
};