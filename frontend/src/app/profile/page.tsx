"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Plus, Sparkles } from "lucide-react"
import { SkillsDataTable } from "@/components/skills-data-table"
import { AddSkillDialog } from "@/components/add-skill-dialog"
import type { Skill, SkillFormData, RecommendationRequest } from "@/types/skill"
import { toast } from "sonner"

const SKILLS_STORAGE_KEY = "user-skills"

export default function ProfilePage() {
  const [skills, setSkills] = useState<Skill[]>([])
  const [isDialogOpen, setIsDialogOpen] = useState(false)
  const [isGenerating, setIsGenerating] = useState(false)
  const [isLoaded, setIsLoaded] = useState(false)
  const router = useRouter()

  // Load skills from localStorage on component mount
  useEffect(() => {
    try {
      const savedSkills = localStorage.getItem(SKILLS_STORAGE_KEY)
      if (savedSkills) {
        const parsedSkills = JSON.parse(savedSkills)
        setSkills(parsedSkills)
      }
    } catch (error) {
      console.error("Error loading skills from localStorage:", error)
    } finally {
      setIsLoaded(true)
    }
  }, [])

  // Save skills to localStorage whenever skills change (but only after initial load)
  useEffect(() => {
    if (isLoaded) {
      try {
        localStorage.setItem(SKILLS_STORAGE_KEY, JSON.stringify(skills))
      } catch (error) {
        console.error("Error saving skills to localStorage:", error)
      }
    }
  }, [skills, isLoaded])

  const handleAddSkill = (data: SkillFormData) => {
    const newSkill: Skill = {
      id: crypto.randomUUID(),
      ...data,
    }
    setSkills((prev) => [...prev, newSkill])
    toast.success("Skill added successfully!")
  }

  const handleDeleteSkill = (id: string) => {
    setSkills((prev) => prev.filter((skill) => skill.id !== id))
    toast.success("Skill deleted successfully!")
  }

  const handleGenerateRecommendations = async () => {
    if (skills.length === 0) {
      toast.error("Please add some skills before generating recommendations.")
      return
    }

    setIsGenerating(true)

    try {
      // Concatenate all descriptions
      const concatenatedDescription = skills
        .map((skill) => skill.description || "")
        .filter(Boolean)
        .join(". ")

      const requestData: RecommendationRequest = {
        skills: skills,
        description: concatenatedDescription || "No description provided",
        top_k: 5,
      }

      // Store the request data in sessionStorage to pass to the recommendations page
      sessionStorage.setItem("recommendationRequest", JSON.stringify(requestData))

      // Navigate to recommendations page
      router.push("/recommendations")
    } catch (error) {
      console.error("Error generating recommendations:", error)
      toast.error("Failed to generate recommendations. Please try again.")
    } finally {
      setIsGenerating(false)
    }
  }

  return (
    <div className="container mx-auto py-8 px-4 max-w-6xl">
      {/* Skills Section */}
      <Card className="border-0 shadow-none">
        <CardHeader>
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <div>
              <CardTitle className="text-2xl">Skills & Expertise</CardTitle>
              <CardDescription>Manage your technical skills and experience levels</CardDescription>
            </div>
            <div className="flex gap-2 shrink-0">
              <Button
                onClick={handleGenerateRecommendations}
                disabled={isGenerating || skills.length === 0}
                variant="outline"
              >
                <Sparkles className="h-4 w-4 mr-2" />
                {isGenerating ? "Generating..." : "Generate Recommendations"}
              </Button>
              <Button onClick={() => setIsDialogOpen(true)}>
                <Plus className="h-4 w-4 mr-2" />
                Add Skill
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <SkillsDataTable skills={skills} onDeleteSkill={handleDeleteSkill} />
        </CardContent>
      </Card>

      {/* Add Skill Dialog */}
      <AddSkillDialog open={isDialogOpen} onOpenChange={setIsDialogOpen} onAddSkill={handleAddSkill} />
    </div>
  )
}
