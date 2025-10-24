import React, { useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Progress } from '@/components/ui/progress';
import { Upload, FileText, Shield, X, CheckCircle2, Loader2, ArrowLeft } from 'lucide-react';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const UploadPage = () => {
  const navigate = useNavigate();
  const [startupName, setStartupName] = useState('');
  const [contactEmail, setContactEmail] = useState('');
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);

  const onDrop = useCallback((acceptedFiles) => {
    const validFiles = acceptedFiles.filter(file => 
      file.name.toLowerCase().endsWith('.pdf') || file.name.toLowerCase().endsWith('.docx')
    );
    
    if (validFiles.length !== acceptedFiles.length) {
      toast.error('Only PDF and DOCX files are accepted');
    }
    
    setFiles(prev => [...prev, ...validFiles]);
    toast.success(`${validFiles.length} file(s) added`);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']
    }
  });

  const removeFile = (index) => {
    setFiles(prev => prev.filter((_, i) => i !== index));
    toast.info('File removed');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!startupName.trim()) {
      toast.error('Please enter your startup name');
      return;
    }

    if (files.length === 0) {
      toast.error('Please upload at least one document');
      return;
    }

    try {
      setUploading(true);
      setProgress(10);

      // Create assessment
      const assessmentResponse = await axios.post(`${API}/assessments`, {
        startup_name: startupName,
        contact_email: contactEmail || null
      });

      const assessmentId = assessmentResponse.data.id;
      setProgress(30);

      // Upload files
      const formData = new FormData();
      files.forEach(file => {
        formData.append('files', file);
      });

      setProgress(50);

      const uploadResponse = await axios.post(
        `${API}/assessments/${assessmentId}/upload`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          onUploadProgress: (progressEvent) => {
            const percentCompleted = Math.round(
              50 + (progressEvent.loaded * 40) / progressEvent.total
            );
            setProgress(percentCompleted);
          }
        }
      );

      setProgress(100);
      toast.success('Documents analyzed successfully!');

      // Navigate to results
      setTimeout(() => {
        navigate(`/results/${assessmentId}`);
      }, 500);

    } catch (error) {
      console.error('Upload error:', error);
      toast.error(error.response?.data?.detail || 'Failed to process documents');
      setUploading(false);
      setProgress(0);
    }
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
                <p className="text-sm text-gray-500">Upload Documents for Assessment</p>
              </div>
            </div>
            <Button 
              onClick={() => navigate('/')} 
              variant="outline"
              data-testid="back-home-btn"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Home
            </Button>
          </div>
        </div>
      </header>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">Start Your Assessment</h2>
          <p className="text-lg text-gray-600">
            Upload your startup documents to receive a comprehensive regulatory readiness analysis
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Startup Information</CardTitle>
              <CardDescription>Tell us about your fintech startup</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="startupName">Startup Name *</Label>
                <Input
                  id="startupName"
                  type="text"
                  placeholder="e.g., Al-Ameen Digital"
                  value={startupName}
                  onChange={(e) => setStartupName(e.target.value)}
                  required
                  data-testid="startup-name-input"
                />
              </div>
              <div>
                <Label htmlFor="contactEmail">Contact Email (Optional)</Label>
                <Input
                  id="contactEmail"
                  type="email"
                  placeholder="contact@example.com"
                  value={contactEmail}
                  onChange={(e) => setContactEmail(e.target.value)}
                  data-testid="contact-email-input"
                />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Document Upload</CardTitle>
              <CardDescription>
                Upload your business plan, legal documents, and compliance policies (PDF or DOCX)
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div
                {...getRootProps()}
                className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-colors ${
                  isDragActive
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-300 hover:border-blue-400'
                }`}
                data-testid="dropzone"
              >
                <input {...getInputProps()} />
                <Upload className="w-12 h-12 mx-auto mb-4 text-gray-400" />
                {isDragActive ? (
                  <p className="text-blue-600 font-medium">Drop the files here...</p>
                ) : (
                  <>
                    <p className="text-gray-700 font-medium mb-2">
                      Drag & drop files here, or click to select
                    </p>
                    <p className="text-sm text-gray-500">
                      Supported formats: PDF, DOCX
                    </p>
                  </>
                )}
              </div>

              {files.length > 0 && (
                <div className="mt-6 space-y-3">
                  <h4 className="font-medium text-gray-900">Uploaded Files ({files.length})</h4>
                  {files.map((file, index) => (
                    <div
                      key={index}
                      className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                      data-testid={`file-item-${index}`}
                    >
                      <div className="flex items-center space-x-3">
                        <FileText className="w-5 h-5 text-blue-600" />
                        <div>
                          <p className="text-sm font-medium text-gray-900">{file.name}</p>
                          <p className="text-xs text-gray-500">
                            {(file.size / 1024).toFixed(2)} KB
                          </p>
                        </div>
                      </div>
                      <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        onClick={() => removeFile(index)}
                        data-testid={`remove-file-${index}`}
                      >
                        <X className="w-4 h-4" />
                      </Button>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>

          {uploading && (
            <Card>
              <CardContent className="pt-6">
                <div className="space-y-3">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-700">Processing documents...</span>
                    <span className="font-medium text-blue-600">{progress}%</span>
                  </div>
                  <Progress value={progress} className="h-2" />
                </div>
              </CardContent>
            </Card>
          )}

          <div className="flex items-center justify-end space-x-4">
            <Button
              type="button"
              variant="outline"
              onClick={() => navigate('/')}
              disabled={uploading}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              disabled={uploading || files.length === 0 || !startupName.trim()}
              className="bg-blue-600 hover:bg-blue-700"
              data-testid="submit-assessment-btn"
            >
              {uploading ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Processing...
                </>
              ) : (
                <>
                  <CheckCircle2 className="w-4 h-4 mr-2" />
                  Analyze Documents
                </>
              )}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default UploadPage;
