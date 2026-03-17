import { useState } from 'react';
import { Navigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { useAuth } from '@/contexts/AuthContext';
import { useLanguage } from '@/contexts/LanguageContext';
import { toast } from 'sonner';
import { Globe, Activity, Brain, Users } from 'lucide-react';
import disabilityHero from '@/assets/disability-hero.jpg';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';

export default function LoginLanding() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [loginType, setLoginType] = useState<'doctor' | 'admin'>('doctor');
  
  const { user, login } = useAuth();
  const { language, setLanguage, t } = useLanguage();

  if (user) {
    return <Navigate to="/dashboard" replace />;
  }

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      await login(email, password);
      toast.success(t('success'));
    } catch (error) {
      // Show user-friendly error message without logging to console
      toast.error(error instanceof Error ? error.message : t('error'));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary/5 via-background to-accent/5">
      {/* Header */}
      <header className="border-b border-border bg-card/50 backdrop-blur">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-primary rounded-lg">
              <Activity className="h-6 w-6 text-primary-foreground" />
            </div>
            <h1 className="text-xl font-bold">Health Access Bridge</h1>
          </div>
          
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="icon" className="rounded-full">
                <Globe className="h-5 w-5" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem onClick={() => setLanguage('en')}>
                <span className={language === 'en' ? 'font-bold' : ''}>English</span>
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => setLanguage('es')}>
                <span className={language === 'es' ? 'font-bold' : ''}>Español</span>
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-16 grid lg:grid-cols-2 gap-12 items-center">
        <div className="space-y-6">
          <h2 className="text-4xl md:text-5xl font-bold leading-tight">
            {language === 'es' 
              ? 'Sistema Inteligente de Perfilamiento de Discapacidad'
              : 'Intelligent Disability Profiling System'}
          </h2>
          <p className="text-lg text-muted-foreground">
            {language === 'es'
              ? 'Herramienta avanzada para profesionales de la salud que facilita la evaluación y predicción de barreras en personas con discapacidad mediante inteligencia artificial.'
              : 'Advanced tool for healthcare professionals that facilitates the assessment and prediction of barriers in people with disabilities using artificial intelligence.'}
          </p>
          
          <div className="grid sm:grid-cols-2 gap-4 pt-4">
            <div className="flex items-start gap-3">
              <Brain className="h-6 w-6 text-primary mt-1" />
              <div>
                <h3 className="font-semibold">
                  {language === 'es' ? 'IA Predictiva' : 'Predictive AI'}
                </h3>
                <p className="text-sm text-muted-foreground">
                  {language === 'es' 
                    ? 'Modelos híbridos de aprendizaje automático'
                    : 'Hybrid machine learning models'}
                </p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <Users className="h-6 w-6 text-primary mt-1" />
              <div>
                <h3 className="font-semibold">
                  {language === 'es' ? 'Gestión de Pacientes' : 'Patient Management'}
                </h3>
                <p className="text-sm text-muted-foreground">
                  {language === 'es' 
                    ? 'Historiales completos y seguimiento'
                    : 'Complete records and tracking'}
                </p>
              </div>
            </div>
          </div>
          
          <div className="mt-8">
            <img 
              src={disabilityHero} 
              alt="Physical disability support and assessment"
              className="rounded-xl shadow-lg w-full object-cover max-h-64"
            />
          </div>
        </div>

        {/* Login Card */}
        <Card className="shadow-xl">
          <CardHeader className="space-y-3">
            <div className="flex gap-2 p-1 bg-muted rounded-lg">
              <Button
                type="button"
                variant={loginType === 'doctor' ? 'default' : 'ghost'}
                className="flex-1"
                onClick={() => setLoginType('doctor')}
              >
                {language === 'es' ? 'Médico' : 'Doctor'}
              </Button>
              <Button
                type="button"
                variant={loginType === 'admin' ? 'default' : 'ghost'}
                className="flex-1"
                onClick={() => setLoginType('admin')}
              >
                {language === 'es' ? 'Administrador' : 'Admin'}
              </Button>
            </div>
            <CardTitle className="text-2xl">
              {loginType === 'admin' 
                ? (language === 'es' ? 'Acceso Administrador' : 'Admin Access')
                : (language === 'es' ? 'Acceso Médico' : 'Doctor Access')}
            </CardTitle>
            <CardDescription>
              {loginType === 'admin'
                ? (language === 'es' 
                  ? 'Gestione usuarios y configuración del sistema'
                  : 'Manage users and system configuration')
                : (language === 'es'
                  ? 'Ingrese sus credenciales para acceder al sistema'
                  : 'Enter your credentials to access the system')}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleLogin} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="email">{t('email')}</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder={loginType === 'admin' ? 'admin@salud.co' : 'doctor@example.com'}
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="password">{t('password')}</Label>
                <Input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>
              <Button type="submit" className="w-full" disabled={isLoading}>
                {isLoading ? t('loading') : t('login')}
              </Button>
            </form>
          </CardContent>
        </Card>
      </section>

      {/* Footer */}
      <footer className="border-t border-border bg-card/50 backdrop-blur mt-16">
        <div className="container mx-auto px-4 py-6 text-center text-sm text-muted-foreground">
          <p>
            {language === 'es' 
              ? 'Desarrollado por: Ing. Julián Andrés Quimbayo Castro'
              : 'Developed by: Eng. Julián Andrés Quimbayo Castro'}
          </p>
        </div>
      </footer>
    </div>
  );
}
