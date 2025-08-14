import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { isValidEmail, validatePassword } from "../utils/validators";
import conpu from "../assets/conpu.jpg"; // 📌 Importar imagen

const LoginScreen = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleLogin = async () => {
    if (isSubmitting) return;
    setError("");
    setIsSubmitting(true);

    if (!email.trim()) {
      setError("El email es requerido");
      setIsSubmitting(false);
      return;
    }

    if (!email.includes("@") || !email.includes(".")) {
      setError("Por favor ingresa un email válido");
      setIsSubmitting(false);
      return;
    }

    if (!password.trim()) {
      setError("La contraseña es requerida");
      setIsSubmitting(false);
      return;
    }

    try {
      console.log("Intentando login con:", { email, password: "***" });
      const result = await login(email, password);
      console.log("Resultado del login:", result);
      if (result) {
        navigate("/dashboard", { replace: true });
      }
    } catch (error) {
      console.error("Error en login:", error);
      setError(error.message || "Error al iniciar sesión. Intenta nuevamente.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-green-100 flex items-center justify-center p-4">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="w-16 h-16 bg-green-400 rounded-full flex items-center justify-center mx-auto mb-4">
            <img
              src={conpu}
              alt="Logo"
              className="w-12 h-12 object-cover rounded-full"
            />
          </div>
          <h1 className="text-2xl font-bold text-gray-800">Components Shop</h1>
          <p className="text-gray-600">Inicia sesión</p>
        </div>

        {/* Mensaje de error */}
        {error && (
          <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded-md">
            <div className="flex items-center">
              <span className="mr-2">❌</span>
              <span>{error}</span>
            </div>
          </div>
        )}

        {/* Formulario */}
        <form className="space-y-4" noValidate>
          <div>
            <label
              htmlFor="email"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Email
            </label>
            <input
              type="email"
              id="email"
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-400"
              placeholder="tu@email.com"
              value={email}
              onChange={(e) => {
                setEmail(e.target.value);
                if (error) setError("");
              }}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  handleLogin();
                }
              }}
            />
          </div>

          <div>
            <label
              htmlFor="password"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Contraseña
            </label>
            <input
              type="password"
              id="password"
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-400"
              placeholder="••••••••"
              value={password}
              onChange={(e) => {
                setPassword(e.target.value);
                if (error) setError("");
              }}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  handleLogin();
                }
              }}
            />
          </div>

          <button
            type="button"
            onClick={handleLogin}
            className="w-full bg-green-400 text-white py-2 px-4 rounded-md hover:bg-green-500 font-medium disabled:opacity-50 disabled:cursor-not-allowed"
            disabled={isSubmitting}
          >
            {isSubmitting ? "Iniciando sesión..." : "Iniciar Sesión"}
          </button>
        </form>

        {/* Link de registro */}
        <p className="text-center text-sm text-gray-600 mt-4">
          ¿No tienes cuenta?{" "}
          <Link
            to="/signup"
            className="text-green-500 hover:text-green-600"
          >
            Regístrate
          </Link>
        </p>
      </div>
    </div>
  );
};

export default LoginScreen;
