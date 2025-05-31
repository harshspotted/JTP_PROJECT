"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { ArrowLeft, Star, Clock, Code, Brain, AlertCircle } from "lucide-react"
import { Skeleton } from "@/components/ui/skeleton"
import type {
  RecommendationRequest,
  RecommendationWithMetaDataResult,
  AnalysisResult,
  AnalysisRequest,
} from "@/types/skill"
import { toast } from "sonner"

export default function RecommendationsPage() {
  const [recommendations, setRecommendations] = useState<RecommendationWithMetaDataResult[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [requestData, setRequestData] = useState<RecommendationRequest | null>(null)
  const [expandedDescriptions, setExpandedDescriptions] = useState<Record<string, boolean>>({})
  const [analysisResults, setAnalysisResults] = useState<Record<string, AnalysisResult>>({})
  const [loadingAnalysis, setLoadingAnalysis] = useState<Record<string, boolean>>({})
  const router = useRouter()

  useEffect(() => {
    const fetchRecommendations = async () => {
      try {
        const storedData = sessionStorage.getItem("recommendationRequest")
        if (!storedData) {
          toast.error("No data found. Please generate recommendations from your profile page.")
          router.push("/profile")
          return
        }

        const data: RecommendationRequest = JSON.parse(storedData)
        setRequestData(data)

        const response = await fetch("/api/recommendations", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        })

        if (!response.ok) {
          throw new Error("Failed to fetch recommendations")
        }

        const result = await response.json()
        setRecommendations(result)
      } catch (error) {
        console.error("Error fetching recommendations:", error)
        toast.error("Failed to fetch recommendations from API.")
        setError("Unable to fetch recommendations. Please try again.")
      } finally {
        setLoading(false)
      }
    }

    fetchRecommendations()
  }, [router])

  const handleGenerateAnalysis = async (recommendation: RecommendationWithMetaDataResult) => {
    if (!requestData) return

    setLoadingAnalysis((prev) => ({ ...prev, [recommendation.project_id]: true }))

    try {
      const analysisRequest: AnalysisRequest = {
        employee_skills: requestData.skills.map((skill) => ({
          skill_name: skill.skill_name,
          level: skill.level,
          months: skill.months,
        })),
        employee_description: requestData.description,
        project_skills: recommendation.required_skills,
        project_description: recommendation.description,
        score: recommendation.score,
      }

      const response = await fetch("/api/analysis", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(analysisRequest),
      })

      if (response.status === 501) {
        const errorData = await response.json()
        toast.error(errorData.error || "Configure LLM Services")
        return
      }

      if (!response.ok) {
        throw new Error("Failed to generate analysis")
      }

      const analysis: AnalysisResult = await response.json()

      setAnalysisResults((prev) => ({
        ...prev,
        [recommendation.project_id]: analysis,
      }))

      toast.success("Analysis generated successfully!")
    } catch (error) {
      console.error("Error generating analysis:", error)
      toast.error("Failed to generate analysis. Please try again.")
    } finally {
      setLoadingAnalysis((prev) => ({ ...prev, [recommendation.project_id]: false }))
    }
  }

  const getScoreColor = (score: number) => {
    const normalizedScore = score > 100 ? score / 1000 : score
    if (normalizedScore >= 50) return "bg-green-100 text-green-800"
    if (normalizedScore >= 30) return "bg-yellow-100 text-yellow-800"
    return "bg-red-100 text-red-800"
  }

  const getLevelColor = (level: string) => {
    const colors = {
      Basic: "bg-blue-100 text-blue-800",
      CollegeResearch: "bg-purple-100 text-purple-800",
      Professional: "bg-green-100 text-green-800",
      Other: "bg-gray-100 text-gray-800",
    }
    return colors[level as keyof typeof colors] || colors.Other
  }

  const toggleDescription = (projectId: string) => {
    setExpandedDescriptions((prev) => ({
      ...prev,
      [projectId]: !prev[projectId],
    }))
  }

  const getTruncatedText = (text: string, isExpanded: boolean, length = 200) => {
    if (isExpanded || text.length <= length) return text
    return text.slice(0, length) + "..."
  }

  if (loading) {
    return (
      <div className="container mx-auto py-8 px-4 max-w-6xl">
        <div className="mb-6">
          <Skeleton className="h-8 w-64 mb-2" />
          <Skeleton className="h-4 w-96" />
        </div>
        <div className="space-y-4">
          {[1, 2, 3].map((i) => (
            <Card key={i}>
              <CardHeader>
                <Skeleton className="h-6 w-48" />
                <Skeleton className="h-4 w-full" />
              </CardHeader>
              <CardContent>
                <Skeleton className="h-20 w-full" />
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="container mx-auto py-8 px-4 max-w-6xl text-center">
        <div className="mb-6">
          <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
          <h2 className="text-2xl font-semibold text-red-600 mb-2">Oops! Something went wrong</h2>
          <p className="text-muted-foreground mb-4">{error}</p>
          <Button onClick={() => router.push("/profile")}>
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Profile
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div className="container mx-auto py-8 px-4 max-w-6xl">
      <div className="mb-8">
        <Button variant="ghost" onClick={() => router.push("/profile")} className="mb-4">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Profile
        </Button>

        <h1 className="text-3xl font-bold mb-2">Project Recommendations</h1>
        <p className="text-muted-foreground">
          Based on your skills and experience, here are {requestData?.top_k || 5} recommended projects
        </p>
      </div>

      {requestData && (
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="text-xl">Employee&apos;s Skills</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              {requestData.skills.map((skill) => (
                <div key={skill.id} className="border rounded-lg p-3 space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="font-medium text-sm">{skill.skill_name}</span>
                    <Badge variant="outline" className={getLevelColor(skill.level)}>
                      {skill.level === "CollegeResearch" ? "College Research" : skill.level}
                    </Badge>
                  </div>
                  <div className="flex items-center gap-1 text-xs text-muted-foreground">
                    <Clock className="h-3 w-3" />
                    {Math.floor(skill.months / 12) > 0
                      ? `${Math.floor(skill.months / 12)}y ${skill.months % 12}m`
                      : `${skill.months}m`}{" "}
                    experience
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      <div className="space-y-6">
        {recommendations.map((recommendation) => (
          <Card key={recommendation.project_id} className="overflow-hidden">
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <div className="flex items-center justify-center w-8 h-8 rounded-full bg-primary text-primary-foreground text-sm font-bold">
                    {recommendation.rank}
                  </div>
                  <div>
                    <CardTitle className="text-xl">{recommendation.project_id}</CardTitle>
                    <div className="flex items-center gap-2 mt-1">
                      <Badge className={getScoreColor(recommendation.score)}>
                        <Star className="h-3 w-3 mr-1" />
                        {recommendation.score > 100
                          ? recommendation.score.toFixed(0)
                          : (recommendation.score * 100).toFixed(0)}{" "}
                        Score
                      </Badge>
                    </div>
                  </div>
                </div>
                <Button
                  onClick={() => handleGenerateAnalysis(recommendation)}
                  disabled={loadingAnalysis[recommendation.project_id]}
                  variant="outline"
                  size="sm"
                >
                  <Brain className="h-4 w-4 mr-2" />
                  {loadingAnalysis[recommendation.project_id] ? "Analyzing..." : "Generate Analysis"}
                </Button>
              </div>
            </CardHeader>

            <CardContent className="space-y-4">

              {/* Analysis Section */}
              {loadingAnalysis[recommendation.project_id] && (
                <div className="space-y-4 border-t pt-4">
                  <h4 className="font-medium flex items-center gap-2">
                    <Brain className="h-4 w-4" />
                    Analysis
                  </h4>
                  <div className="space-y-3">
                    <div>
                      <Skeleton className="h-4 w-32 mb-2" />
                      <Skeleton className="h-16 w-full" />
                    </div>
                    <div>
                      <Skeleton className="h-4 w-40 mb-2" />
                      <Skeleton className="h-16 w-full" />
                    </div>
                  </div>
                </div>
              )}

              {analysisResults[recommendation.project_id] && (
                <div className="space-y-4 border-t pt-4">
                  <h4 className="font-medium flex items-center gap-2">
                    <Brain className="h-4 w-4" />
                    Analysis
                  </h4>
                  <div className="space-y-3">
                    <div>
                      <h5 className="text-sm font-medium mb-2">Employee Evaluation</h5>
                      <p className="text-sm text-muted-foreground leading-relaxed bg-muted/50 p-3 rounded-lg">
                        {analysisResults[recommendation.project_id].fitness_evaluation}
                      </p>
                    </div>
                    <div>
                      <h5 className="text-sm font-medium mb-2">Recommended Courses</h5>
                      <p className="text-sm text-muted-foreground leading-relaxed bg-muted/50 p-3 rounded-lg">
                        {analysisResults[recommendation.project_id].recommended_courses}
                      </p>
                    </div>
                  </div>
                </div>
              )}

              <div>
                <h4 className="font-medium mb-3 flex items-center gap-2">
                  <Code className="h-4 w-4" />
                  Required Skills
                </h4>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                  {recommendation.required_skills.map((skill, index) => (
                    <div key={index} className="border rounded-lg p-3 space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="font-medium text-sm">{skill.skill_name}</span>
                        <Badge variant="outline" className={getLevelColor(skill.level)}>
                          {skill.level === "CollegeResearch" ? "College Research" : skill.level}
                        </Badge>
                      </div>
                      <div className="flex items-center gap-1 text-xs text-muted-foreground">
                        <Clock className="h-3 w-3" />
                        {Math.floor(skill.months / 12) > 0
                          ? `${Math.floor(skill.months / 12)}y ${skill.months % 12}m`
                          : `${skill.months}m`}{" "}
                        experience
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div>
                <h4 className="font-medium mb-2">Project Description</h4>
                <p className="text-muted-foreground leading-relaxed">
                  {getTruncatedText(recommendation.description, expandedDescriptions[recommendation.project_id])}
                </p>
                {recommendation.description.length > 200 && (
                  <Button
                    variant="link"
                    className="text-sm mt-1 px-0"
                    onClick={() => toggleDescription(recommendation.project_id)}
                  >
                    {expandedDescriptions[recommendation.project_id] ? "Show Less" : "Read More"}
                  </Button>
                )}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {recommendations.length === 0 && !loading && !error && (
        <Card>
          <CardContent className="py-12 text-center">
            <h3 className="text-lg font-semibold text-muted-foreground mb-2">No recommendations found</h3>
            <p className="text-sm text-muted-foreground">
              Try adding more skills to your profile to get better recommendations.
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
