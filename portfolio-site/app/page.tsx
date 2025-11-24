import { Github, Linkedin, Mail, ExternalLink, Code, Activity } from 'lucide-react'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 text-white">
      {/* Header */}
      <header className="container mx-auto px-6 py-8">
        <nav className="flex justify-between items-center">
          <h1 className="text-2xl font-bold">Rogério Tavares</h1>
          <div className="flex gap-4">
            <a href="https://github.com/rogtavares" className="hover:text-strava transition-colors">
              <Github size={24} />
            </a>
            <a href="mailto:contato@rogtavares.dev" className="hover:text-strava transition-colors">
              <Mail size={24} />
            </a>
          </div>
        </nav>
      </header>

      {/* Hero */}
      <section className="container mx-auto px-6 py-16 text-center">
        <h2 className="text-5xl font-bold mb-6">Desenvolvedor Java & APIs</h2>
        <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
          Especialista em integração de APIs, OAuth 2.0 e desenvolvimento de aplicações Java. 
          Apaixonado por dados esportivos e tecnologia.
        </p>
        <div className="flex gap-4 justify-center">
          <a href="#projetos" className="bg-strava hover:bg-orange-600 px-6 py-3 rounded-lg font-semibold transition-colors">
            Ver Projetos
          </a>
          <a href="https://github.com/rogtavares" className="border border-gray-600 hover:border-strava px-6 py-3 rounded-lg font-semibold transition-colors">
            GitHub
          </a>
        </div>
      </section>

      {/* Projetos */}
      <section id="projetos" className="container mx-auto px-6 py-16">
        <h3 className="text-3xl font-bold mb-12 text-center">Projetos em Destaque</h3>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {/* Projeto Strava */}
          <div className="bg-gray-800 rounded-lg p-6 hover:bg-gray-750 transition-colors">
            <div className="flex items-center mb-4">
              <Activity className="text-strava mr-3" size={24} />
              <h4 className="text-xl font-semibold">Strava API Integration</h4>
            </div>
            <p className="text-gray-300 mb-4">
              Integração completa com API do Strava usando OAuth 2.0, Java 17+ e Apache HttpClient.
            </p>
            <div className="flex flex-wrap gap-2 mb-4">
              <span className="bg-blue-600 px-2 py-1 rounded text-sm">Java</span>
              <span className="bg-green-600 px-2 py-1 rounded text-sm">OAuth 2.0</span>
              <span className="bg-strava px-2 py-1 rounded text-sm">Strava API</span>
            </div>
            <div className="flex gap-2">
              <a href="https://github.com/rogtavares/strava-connect-java-getavares" 
                 className="flex items-center text-strava hover:underline">
                <Github size={16} className="mr-1" />
                Código
              </a>
              <a href="#" className="flex items-center text-gray-400 hover:text-white">
                <ExternalLink size={16} className="mr-1" />
                Demo
              </a>
            </div>
          </div>

          {/* Projeto Dashboard Climático */}
          <div className="bg-gray-800 rounded-lg p-6 hover:bg-gray-750 transition-colors">
            <div className="flex items-center mb-4">
              <Code className="text-blue-400 mr-3" size={24} />
              <h4 className="text-xl font-semibold">Dashboard Climático</h4>
            </div>
            <p className="text-gray-300 mb-4">
              Dashboard interativo com dados meteorológicos, gráficos e previsões usando OpenWeather API.
            </p>
            <div className="flex flex-wrap gap-2 mb-4">
              <span className="bg-yellow-600 px-2 py-1 rounded text-sm">React</span>
              <span className="bg-blue-600 px-2 py-1 rounded text-sm">API REST</span>
              <span className="bg-green-600 px-2 py-1 rounded text-sm">Charts.js</span>
            </div>
            <div className="flex gap-2">
              <a href="#" className="flex items-center text-strava hover:underline">
                <Github size={16} className="mr-1" />
                Código
              </a>
              <a href="#" className="flex items-center text-gray-400 hover:text-white">
                <ExternalLink size={16} className="mr-1" />
                Demo
              </a>
            </div>
          </div>

          {/* Projeto Treino + Clima */}
          <div className="bg-gray-800 rounded-lg p-6 hover:bg-gray-750 transition-colors">
            <div className="flex items-center mb-4">
              <Activity className="text-green-400 mr-3" size={24} />
              <h4 className="text-xl font-semibold">Treino + Clima Analytics</h4>
            </div>
            <p className="text-gray-300 mb-4">
              Análise correlacional entre performance esportiva e condições climáticas com IA generativa.
            </p>
            <div className="flex flex-wrap gap-2 mb-4">
              <span className="bg-purple-600 px-2 py-1 rounded text-sm">Spring Boot</span>
              <span className="bg-orange-600 px-2 py-1 rounded text-sm">AWS Bedrock</span>
              <span className="bg-blue-600 px-2 py-1 rounded text-sm">PostgreSQL</span>
            </div>
            <div className="flex gap-2">
              <a href="#" className="flex items-center text-strava hover:underline">
                <Github size={16} className="mr-1" />
                Código
              </a>
              <a href="#" className="flex items-center text-gray-400 hover:text-white">
                <ExternalLink size={16} className="mr-1" />
                Demo
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Tecnologias */}
      <section className="container mx-auto px-6 py-16">
        <h3 className="text-3xl font-bold mb-12 text-center">Tecnologias</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
          <div className="bg-gray-800 p-4 rounded-lg">
            <h4 className="font-semibold mb-2">Backend</h4>
            <p className="text-gray-300 text-sm">Java, Spring Boot, Maven</p>
          </div>
          <div className="bg-gray-800 p-4 rounded-lg">
            <h4 className="font-semibold mb-2">Frontend</h4>
            <p className="text-gray-300 text-sm">React, Next.js, TailwindCSS</p>
          </div>
          <div className="bg-gray-800 p-4 rounded-lg">
            <h4 className="font-semibold mb-2">APIs</h4>
            <p className="text-gray-300 text-sm">REST, OAuth 2.0, OpenAPI</p>
          </div>
          <div className="bg-gray-800 p-4 rounded-lg">
            <h4 className="font-semibold mb-2">Cloud</h4>
            <p className="text-gray-300 text-sm">AWS, Lambda, API Gateway</p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="container mx-auto px-6 py-8 text-center text-gray-400">
        <p>&copy; 2025 Rogério Tavares. Desenvolvido com Next.js e TailwindCSS.</p>
      </footer>
    </div>
  )
}