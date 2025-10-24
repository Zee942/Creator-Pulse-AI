import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Shield, ArrowLeft, AlertTriangle, CheckCircle2, XCircle, Users, BookOpen, Loader2, TrendingUp, AlertCircle } from 'lucide-react';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const ResultsPage = () => {
  const { assessmentId } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [result, setResult] = useState(null);

  useEffect(() => {
    fetchResults();
  }, [assessmentId]);

  const fetchResults = async () => {
    try {
      const response = await axios.get(`${API}/assessments/${assessmentId}`);
      setResult(response.data);
    } catch (error) {
      console.error('Error fetching results:', error);
      toast.error('Failed to load assessment results');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 to-slate-100">
        <div className="text-center">
          <Loader2 className="w-12 h-12 animate-spin text-blue-600 mx-auto mb-4" />
          <p className="text-gray-600">Loading assessment results...</p>
        </div>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 to-slate-100">
        <Card className="max-w-md">
          <CardHeader>
            <CardTitle>Assessment Not Found</CardTitle>
            <CardDescription>The requested assessment could not be found</CardDescription>
          </CardHeader>
          <CardContent>
            <Button onClick={() => navigate('/')}>Return to Home</Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  const { startup_name, score, gaps, recommendations } = result;

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'HIGH':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'MEDIUM':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'LOW':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getScoreColor = (scoreValue) => {
    if (scoreValue >= 75) return 'text-green-600';
    if (scoreValue >= 50) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Shield className="w-10 h-10 text-blue-600" />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">FinRegX</h1>
                <p className="text-sm text-gray-500">Assessment Results</p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <Button onClick={() => navigate('/upload')} variant="outline">
                New Assessment
              </Button>
              <Button onClick={() => navigate('/')} variant="outline">
                <ArrowLeft className="w-4 h-4 mr-2" />
                Back to Home
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">{startup_name}</h2>
          <p className="text-lg text-gray-600">Regulatory Readiness Assessment Report</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <Card className="lg:col-span-2" data-testid="overall-score-card">
            <CardHeader>
              <CardTitle className="flex items-center">
                <TrendingUp className="w-5 h-5 mr-2" />
                Overall Readiness Score
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-center mb-6">
                <div className={`text-6xl font-bold mb-2 ${getScoreColor(score.overall_score)}`}>
                  {score.overall_score}%
                </div>
                <Badge variant="outline" className="text-lg px-4 py-1">
                  {score.readiness_level}
                </Badge>
              </div>
              
              <div className="space-y-4">
                {Object.entries(score.category_scores).map(([category, categoryScore]) => (
                  <div key={category}>
                    <div className="flex justify-between text-sm mb-2">
                      <span className="font-medium">{category}</span>
                      <span className={getScoreColor(categoryScore)}>{categoryScore}%</span>
                    </div>
                    <Progress value={categoryScore} className="h-2" />
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card data-testid="gaps-summary-card">
            <CardHeader>
              <CardTitle className="flex items-center">
                <AlertCircle className="w-5 h-5 mr-2" />
                Gaps Summary
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Total Gaps</span>
                  <span className="text-2xl font-bold">{score.total_gaps}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-red-600 flex items-center">
                    <XCircle className="w-4 h-4 mr-1" />
                    High Severity
                  </span>
                  <span className="text-2xl font-bold text-red-600">{score.high_severity_gaps}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-yellow-600 flex items-center">
                    <AlertTriangle className="w-4 h-4 mr-1" />
                    Medium Severity
                  </span>
                  <span className="text-2xl font-bold text-yellow-600">{score.medium_severity_gaps}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-blue-600 flex items-center">
                    <CheckCircle2 className="w-4 h-4 mr-1" />
                    Low Severity
                  </span>
                  <span className="text-2xl font-bold text-blue-600">{score.low_severity_gaps}</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        <Tabs defaultValue="gaps" className="space-y-6">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="gaps">Compliance Gaps</TabsTrigger>
            <TabsTrigger value="recommendations">Recommendations</TabsTrigger>
          </TabsList>

          <TabsContent value="gaps" className="space-y-4" data-testid="gaps-tab">
            <Card>
              <CardHeader>
                <CardTitle>Detected Compliance Gaps</CardTitle>
                <CardDescription>
                  Identified issues requiring attention to meet QCB regulatory requirements
                </CardDescription>
              </CardHeader>
              <CardContent>
                {gaps.length === 0 ? (
                  <div className="text-center py-8">
                    <CheckCircle2 className="w-12 h-12 text-green-600 mx-auto mb-3" />
                    <p className="text-lg font-medium text-gray-900">No compliance gaps detected!</p>
                    <p className="text-gray-600">Your startup meets all regulatory requirements</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {gaps.map((gap, index) => (
                      <Card key={index} className="border-l-4" style={{ borderLeftColor: gap.severity === 'HIGH' ? '#dc2626' : gap.severity === 'MEDIUM' ? '#ca8a04' : '#2563eb' }} data-testid={`gap-item-${index}`}>
                        <CardHeader>
                          <div className="flex items-start justify-between">
                            <div className="flex-1">
                              <div className="flex items-center space-x-2 mb-2">
                                <Badge variant="outline" className={getSeverityColor(gap.severity)}>
                                  {gap.severity}
                                </Badge>
                                <Badge variant="outline">{gap.category}</Badge>
                              </div>
                              <CardTitle className="text-lg">{gap.article_name}</CardTitle>
                            </div>
                          </div>
                        </CardHeader>
                        <CardContent className="space-y-3">
                          <div>
                            <p className="text-sm font-medium text-gray-700 mb-1">Issue:</p>
                            <p className="text-sm text-gray-600">{gap.description}</p>
                          </div>
                          <div>
                            <p className="text-sm font-medium text-gray-700 mb-1">Requirement:</p>
                            <p className="text-sm text-gray-600">{gap.requirement}</p>
                          </div>
                          <div className="bg-blue-50 border border-blue-200 rounded p-3">
                            <p className="text-sm font-medium text-blue-900 mb-1">Recommendation:</p>
                            <p className="text-sm text-blue-800">{gap.recommendation}</p>
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="recommendations" className="space-y-6" data-testid="recommendations-tab">
            {recommendations.experts && recommendations.experts.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Users className="w-5 h-5 mr-2" />
                    Expert Recommendations
                  </CardTitle>
                  <CardDescription>
                    Connect with QDB specialists to address your compliance gaps
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {recommendations.experts.map((expert, index) => (
                      <Card key={index} className="border border-blue-200" data-testid={`expert-item-${index}`}>
                        <CardHeader>
                          <CardTitle className="text-lg">{expert.name}</CardTitle>
                          <CardDescription>{expert.specialization}</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-2">
                          <div className="flex items-center text-sm text-gray-600">
                            <span className="font-medium mr-2">Contact:</span>
                            <span>{expert.contact}</span>
                          </div>
                          <div className="flex flex-wrap gap-2">
                            {expert.relevant_articles.map((article, idx) => (
                              <Badge key={idx} variant="outline">Article {article}</Badge>
                            ))}
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}

            {recommendations.programs && recommendations.programs.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <BookOpen className="w-5 h-5 mr-2" />
                    QDB Programs
                  </CardTitle>
                  <CardDescription>
                    Accelerate your licensing journey with specialized support programs
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {recommendations.programs.map((program, index) => (
                      <Card key={index} className="border border-green-200" data-testid={`program-item-${index}`}>
                        <CardHeader>
                          <CardTitle className="text-lg">{program.name}</CardTitle>
                          <CardDescription>{program.description}</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-3">
                          <div className="flex items-center text-sm text-gray-600">
                            <span className="font-medium mr-2">Duration:</span>
                            <span>{program.duration}</span>
                          </div>
                          <div>
                            <p className="text-sm font-medium text-gray-700 mb-2">Focus Areas:</p>
                            <div className="flex flex-wrap gap-2">
                              {program.focus_areas.map((area, idx) => (
                                <Badge key={idx} variant="secondary">{area}</Badge>
                              ))}
                            </div>
                          </div>
                          {program.website !== 'N/A' && (
                            <Button variant="outline" size="sm" asChild>
                              <a href={program.website} target="_blank" rel="noopener noreferrer">
                                Learn More
                              </a>
                            </Button>
                          )}
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
          </TabsContent>
        </Tabs>

        <Card className="mt-8 bg-gradient-to-r from-blue-50 to-indigo-50 border-blue-200">
          <CardContent className="pt-6">
            <div className="text-center">
              <h3 className="text-xl font-bold text-gray-900 mb-2">Need Help?</h3>
              <p className="text-gray-600 mb-4">
                Our team is here to guide you through the licensing process
              </p>
              <Button className="bg-blue-600 hover:bg-blue-700">
                Schedule Expert Consultation
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default ResultsPage;
