import { type NextRequest, NextResponse } from "next/server"
import type { RecommendationRequest, RecommendationWithMetaDataResult } from "@/types/skill"

export async function POST(request: NextRequest) {
  try {
    const body: RecommendationRequest = await request.json()

    // Validate request
    if (!body.skills || body.skills.length === 0) {
      return NextResponse.json({ error: "Skills are required" }, { status: 400 })
    }

    // Get the inference API URL from environment variables
    const inferenceApiUrl = process.env.NEXT_PUBLIC_INFERENCE_API_URL || "http://localhost:8001"

    // Call the actual prediction API
    const response = await fetch(`${inferenceApiUrl}/predict/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        skills: body.skills.map((skill) => ({
          skill_name: skill.skill_name,
          level: skill.level,
          months: skill.months,
        })),
        description: body.description,
        top_k: body.top_k,
      }),
    })

    if (!response.ok) {
      console.error(`API Error: ${response.status} ${response.statusText}`)
      throw new Error(`API request failed: ${response.status}`)
    }

    const recommendations: RecommendationWithMetaDataResult[] = await response.json()

    return NextResponse.json(recommendations)
  } catch (error) {
    console.error("Error in recommendations API:", error)
    return NextResponse.error()
  }
}
