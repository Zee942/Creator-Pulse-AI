import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { FileText, Shield, TrendingUp, CheckCircle2, Upload, Brain, Zap } from 'lucide-react';

const Dashboard = () => {
  const navigate = useNavigate();

  const features = [
    {
      icon: <Brain className="w-8 h-8 text-blue-600" />,
      title: 'AI-Powered Analysis',
      description: 'Advanced NLP and machine learning to parse and understand complex regulatory requirements'
    },
    {
      icon: <Shield className="w-8 h-8 text-green-600" />,
      title: 'Regulatory Mapping',
      description: 'Automatically map your documents to QCB Articles 1.1-2.2 with high precision'
    },
    {
      icon: <TrendingUp className="w-8 h-8 text-purple-600" />,
      title: 'Readiness Scorecard',
      description: 'Get weighted compliance scores across Capital, Governance, AML, and Data Protection'
    },
    {
      icon: <CheckCircle2 className="w-8 h-8 text-indigo-600" />,
      title: 'Gap Detection',
      description: 'Identify specific compliance gaps with severity levels and actionable recommendations'
    }
  ];

  return (
    <div className="min-h-screen">
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Shield className="w-10 h-10 text-blue-600" />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">FinRegX</h1>
                <p className="text-sm text-gray-500">Smart Regulatory Readiness Platform</p>
              </div>
            </div>
            <Button 
              onClick={() => navigate('/upload')} 
              size="lg"
              className="bg-blue-600 hover:bg-blue-700"
              data-testid="start-assessment-btn"
            >
              <Upload className="w-4 h-4 mr-2" />
              Start Assessment
            </Button>
          </div>
        </div>
      </header>

      <div className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center">
            <div className="inline-flex items-center space-x-2 bg-white/10 backdrop-blur-sm rounded-full px-4 py-2 mb-6">
              <Zap className="w-4 h-4" />
              <span className="text-sm font-medium">AIX Hackathon 2025 - Fintech Use Case</span>
            </div>
            <h2 className="text-5xl font-extrabold mb-6">
              Automate Your QCB Licensing
              <br />
              <span className="text-blue-200">Pre-Screening Process</span>
            </h2>
            <p className="text-xl text-blue-100 mb-8 max-w-3xl mx-auto">
              FinRegX uses AI to analyze your startup documents against Qatar Central Bank regulations,
              providing instant compliance gap analysis and expert recommendations.
            </p>
            <div className="flex items-center justify-center space-x-4">
              <Button 
                onClick={() => navigate('/upload')} 
                size="lg"
                className="bg-white text-blue-600 hover:bg-blue-50 font-semibold px-8"
                data-testid="hero-upload-btn"
              >
                <Upload className="w-5 h-5 mr-2" />
                Upload Documents
              </Button>
              <Button 
                variant="outline" 
                size="lg"
                className="border-white text-white hover:bg-white/10"
              >
                <FileText className="w-5 h-5 mr-2" />
                View Demo
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-12">
          <h3 className="text-3xl font-bold text-gray-900 mb-4">How It Works</h3>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Our platform streamlines the QCB licensing pre-screening process with intelligent automation
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {features.map((feature, index) => (
            <Card key={index} className="hover:shadow-lg transition-shadow" data-testid={`feature-card-${index}`}>
              <CardHeader>
                <div className="flex items-center space-x-3 mb-2">
                  {feature.icon}
                  <CardTitle className="text-xl">{feature.title}</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-base">{feature.description}</CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      <div className="bg-white border-y border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold text-blue-600 mb-2">&lt;30s</div>
              <div className="text-gray-600">Average Processing Time</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-green-600 mb-2">&gt;90%</div>
              <div className="text-gray-600">Mapping Accuracy</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-purple-600 mb-2">70%</div>
              <div className="text-gray-600">Time Reduction</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-indigo-600 mb-2">4</div>
              <div className="text-gray-600">QCB Categories Covered</div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <Card className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white border-0">
          <CardHeader className="text-center pb-4">
            <CardTitle className="text-3xl font-bold mb-2">Ready to Get Started?</CardTitle>
            <CardDescription className="text-blue-100 text-lg">
              Upload your startup documents and get your regulatory readiness assessment in minutes
            </CardDescription>
          </CardHeader>
          <CardContent className="text-center">
            <Button 
              onClick={() => navigate('/upload')} 
              size="lg"
              className="bg-white text-blue-600 hover:bg-blue-50 font-semibold px-8"
              data-testid="cta-start-btn"
            >
              <Upload className="w-5 h-5 mr-2" />
              Start Your Assessment Now
            </Button>
          </CardContent>
        </Card>
      </div>

      <footer className="bg-gray-900 text-gray-400">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
            <p>&copy; 2025 FinRegX. Built for AIX Hackathon - Qatar Central Bank Fintech Use Case</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Dashboard;
