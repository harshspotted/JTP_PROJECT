import { type NextRequest, NextResponse } from "next/server"
import type { AnalysisRequest, AnalysisResult } from "@/types/skill"

export async function POST(request: NextRequest) {
  try {
    const body: AnalysisRequest = await request.json()

    // Validate request
    if (!body.employee_skills || body.employee_skills.length === 0) {
      return NextResponse.json({ error: "Employee skills are required" }, { status: 400 })
    }

    if (!body.project_skills || body.project_skills.length === 0) {
      return NextResponse.json({ error: "Project skills are required" }, { status: 400 })
    }

    // Get the inference API URL from environment variables
    const inferenceApiUrl = process.env.NEXT_PUBLIC_INFERENCE_API_URL || "http://localhost:8001"

    // Call the actual analysis API
    const response = await fetch(`${inferenceApiUrl}/analysis/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        employee_skills: body.employee_skills,
        employee_description: body.employee_description,
        project_skills: body.project_skills,
        project_description: body.project_description,
        score: body.score,
      }),
    })

    if (response.status === 501) {
      return NextResponse.json({ error: "Configure LLM Services" }, { status: 501 })
    }

    if (!response.ok) {
      console.error(`API Error: ${response.status} ${response.statusText}`)
      throw new Error(`API request failed: ${response.status}`)
    }

    const analysis: AnalysisResult = await response.json()

    return NextResponse.json(analysis)
  } catch (error) {
    console.error("Error in analysis API:", error)
    return NextResponse.json({ error: "Internal server error" }, { status: 500 })
  }
}
