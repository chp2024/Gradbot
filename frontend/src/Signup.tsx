import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";

function Signup() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
  });

  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    navigate("/chat")
  };


  const renderSignupForm = () => {
    return (
      <div className="flex flex-col items-center justify-center h-full text-center">
        <h1 className="text-4xl font-bold mb-6">Create Your Account</h1>
        <form onSubmit={handleSubmit} className="space-y-4 w-96">
          <Input
            name="name"
            placeholder="Name"
            value={formData.name}
            required
          />
          <Input
            name="email"
            placeholder="Email"
            value={formData.email}
            required
          />
          <Input
            name="password"
            placeholder="Password"
            value={formData.password}
            required
          />
          <Button type="submit" className="w-full">Sign Up</Button>
        </form>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900 flex flex-col">
      <div className="fixed top-4 left-4">
        <img src="../public/howard.png" alt="Logo" className="h-14 w-auto" />
      </div>

      <div className="flex-1 overflow-auto p-6">
        <div className="max-w-xl mx-auto">
          {renderSignupForm()}
        </div>
      </div>
    </div>
  );
}

export default Signup;
