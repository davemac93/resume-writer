"use client";
import { useState, useEffect } from "react";
import { useMutation } from "@tanstack/react-query";
import { getAccessToken } from "../lib/supabaseClient";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Textarea } from "./ui/textarea";
import { Bot, CheckCircle, ArrowRight, Loader2, X, MessageCircle } from "lucide-react";

interface ProfileCompletionDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onComplete: (completedProfile: any) => void;
  initialProfile: any;
}

interface QuestionData {
  question: string;
  suggestions: string[];
  field: string;
  required: boolean;
  context: string;
}

interface CompletionState {
  status: 'question' | 'complete' | 'error';
  question?: QuestionData;
  analysis?: any;
  profile: any;
  message?: string;
}

export default function ProfileCompletionDialog({
  isOpen,
  onClose,
  onComplete,
  initialProfile
}: ProfileCompletionDialogProps) {
  const [completionState, setCompletionState] = useState<CompletionState | null>(null);
  const [userResponse, setUserResponse] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);

  // Start profile completion mutation
  const startCompletionMutation = useMutation({
    mutationFn: async (profile: any) => {
      const token = await getAccessToken();
      if (!token) throw new Error("Not authenticated");

      const res = await fetch("http://localhost:8000/start-profile-completion/", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ profile }),
      });
      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || "Failed to start profile completion");
      }
      return res.json();
    },
    onSuccess: (data) => {
      setCompletionState(data);
    },
  });

  // Process response mutation
  const processResponseMutation = useMutation({
    mutationFn: async ({ profile, field, response, analysis }: {
      profile: any;
      field: string;
      response: string;
      analysis: any;
    }) => {
      const token = await getAccessToken();
      if (!token) throw new Error("Not authenticated");

      const res = await fetch("http://localhost:8000/process-profile-response/", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ profile, field, response, analysis }),
      });
      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || "Failed to process response");
      }
      return res.json();
    },
    onSuccess: (data) => {
      setCompletionState(data);
      if (data.status === 'complete') {
        onComplete(data.profile);
        onClose();
      }
    },
  });

  // Start completion when dialog opens
  useEffect(() => {
    if (isOpen && initialProfile) {
      startCompletionMutation.mutate(initialProfile);
    }
  }, [isOpen, initialProfile]);

  const handleSubmitResponse = () => {
    if (!completionState?.question || !userResponse.trim()) return;

    setIsProcessing(true);
    processResponseMutation.mutate({
      profile: completionState.profile,
      field: completionState.question.field,
      response: userResponse,
      analysis: completionState.analysis
    });
  };

  const handleSuggestionClick = (suggestion: string) => {
    setUserResponse(suggestion);
  };

  const handleSkip = () => {
    if (!completionState?.question) return;

    setIsProcessing(true);
    processResponseMutation.mutate({
      profile: completionState.profile,
      field: completionState.question.field,
      response: "",
      analysis: completionState.analysis
    });
  };

  const resetDialog = () => {
    setCompletionState(null);
    setUserResponse("");
    setIsProcessing(false);
  };

  const handleClose = () => {
    resetDialog();
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center">
              <div className="p-2 bg-blue-100 rounded-full mr-3">
                <Bot className="w-6 h-6 text-blue-600" />
              </div>
              <h2 className="text-2xl font-bold text-gray-900">AI Profile Assistant</h2>
            </div>
            <Button
              onClick={handleClose}
              variant="outline"
              size="sm"
            >
              <X className="w-4 h-4" />
            </Button>
          </div>

          {/* Content */}
          {startCompletionMutation.isPending && (
            <div className="text-center py-8">
              <Loader2 className="w-8 h-8 animate-spin text-blue-600 mx-auto mb-4" />
              <p className="text-gray-600">Analyzing your profile...</p>
            </div>
          )}

          {startCompletionMutation.isError && (
            <div className="bg-red-50 border-2 border-red-200 rounded-lg p-4 mb-6">
              <p className="text-red-600">
                Error: {startCompletionMutation.error?.message}
              </p>
            </div>
          )}

          {completionState?.status === 'complete' && (
            <div className="text-center py-8">
              <CheckCircle className="w-16 h-16 text-green-600 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Profile Complete!</h3>
              <p className="text-gray-600 mb-6">
                {completionState.message || "Your profile is now ready for resume generation."}
              </p>
              <Button
                onClick={() => {
                  onComplete(completionState.profile);
                  handleClose();
                }}
                className="bg-green-600 hover:bg-green-700"
              >
                <CheckCircle className="w-4 h-4 mr-2" />
                Continue to Resume Generation
              </Button>
            </div>
          )}

          {completionState?.status === 'question' && completionState.question && (
            <div className="space-y-6">
              {/* Progress indicator */}
              <div className="bg-blue-50 border-2 border-blue-200 rounded-lg p-4">
                <div className="flex items-center">
                  <MessageCircle className="w-5 h-5 text-blue-600 mr-2" />
                  <span className="text-blue-800 font-medium">
                    {completionState.question.required ? "Required Information" : "Recommended Information"}
                  </span>
                </div>
                {completionState.question.context && (
                  <p className="text-blue-600 text-sm mt-1">
                    {completionState.question.context}
                  </p>
                )}
              </div>

              {/* Question */}
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-3">
                  {completionState.question.question}
                </h3>
                
                {/* Input field */}
                <div className="space-y-4">
                  {completionState.question.field === 'summary' ? (
                    <Textarea
                      value={userResponse}
                      onChange={(e) => setUserResponse(e.target.value)}
                      placeholder="Enter your professional summary..."
                      rows={4}
                      className="w-full"
                    />
                  ) : completionState.question.field === 'work_experience' || completionState.question.field === 'education' ? (
                    <Textarea
                      value={userResponse}
                      onChange={(e) => setUserResponse(e.target.value)}
                      placeholder="Enter your work experience or education details..."
                      rows={6}
                      className="w-full"
                    />
                  ) : (
                    <Input
                      value={userResponse}
                      onChange={(e) => setUserResponse(e.target.value)}
                      placeholder={`Enter your ${completionState.question.field.replace('_', ' ')}...`}
                      className="w-full"
                    />
                  )}

                  {/* Suggestions */}
                  {completionState.question.suggestions.length > 0 && (
                    <div>
                      <p className="text-sm font-medium text-gray-700 mb-2">Suggestions:</p>
                      <div className="flex flex-wrap gap-2">
                        {completionState.question.suggestions.map((suggestion, index) => (
                          <Button
                            key={index}
                            onClick={() => handleSuggestionClick(suggestion)}
                            variant="outline"
                            size="sm"
                            className="text-xs"
                          >
                            {suggestion}
                          </Button>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>

              {/* Actions */}
              <div className="flex justify-between">
                <div className="flex gap-2">
                  <Button
                    onClick={handleSkip}
                    variant="outline"
                    disabled={isProcessing}
                  >
                    Skip
                  </Button>
                </div>
                <div className="flex gap-2">
                  <Button
                    onClick={handleSubmitResponse}
                    disabled={!userResponse.trim() || isProcessing}
                    className="bg-blue-600 hover:bg-blue-700"
                  >
                    {isProcessing ? (
                      <Loader2 className="w-4 h-4 animate-spin mr-2" />
                    ) : (
                      <ArrowRight className="w-4 h-4 mr-2" />
                    )}
                    {isProcessing ? 'Processing...' : 'Continue'}
                  </Button>
                </div>
              </div>

              {/* Processing indicator */}
              {isProcessing && (
                <div className="text-center py-4">
                  <Loader2 className="w-6 h-6 animate-spin text-blue-600 mx-auto mb-2" />
                  <p className="text-gray-600">Processing your response...</p>
                </div>
              )}
            </div>
          )}

          {processResponseMutation.isError && (
            <div className="bg-red-50 border-2 border-red-200 rounded-lg p-4 mt-4">
              <p className="text-red-600">
                Error: {processResponseMutation.error?.message}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
