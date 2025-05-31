"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import type { SkillName, SkillLevel, SkillFormData } from "@/types/skill"

const SKILL_OPTIONS: SkillName[] = [
  "Python",
  "AI and Machine learning",
  "Git",
  "MongoDB",
  "SQL",
  "Docker",
  "Excel",
  "Javascript",
  "Cloud Platform",
]

const LEVEL_OPTIONS: SkillLevel[] = ["Basic", "CollegeResearch", "Professional", "Other"]

interface SkillFormProps {
  onSubmit: (data: SkillFormData) => void
  onCancel: () => void
}

export function SkillForm({ onSubmit, onCancel }: SkillFormProps) {
  const [formData, setFormData] = useState<SkillFormData>({
    skill_name: "Python",
    level: "Basic",
    months: 5,
    description: "",
  })

  const [errors, setErrors] = useState<Partial<Record<keyof SkillFormData, string>>>({})

  const validateForm = (): boolean => {
    const newErrors: Partial<Record<keyof SkillFormData, string>> = {}

    if (!formData.skill_name) {
      newErrors.skill_name = "Skill is required"
    }

    if (!formData.level) {
      newErrors.level = "Level is required"
    }

    if (formData.months < 0) {
      newErrors.months = "Months must be 0 or greater"
    }

    if (!formData.description.trim()) {
      newErrors.description = "Description is required"
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (validateForm()) {
      onSubmit(formData)
    }
  }

  const updateField = <K extends keyof SkillFormData>(field: K, value: SkillFormData[K]) => {
    setFormData((prev) => ({ ...prev, [field]: value }))
    if (errors[field]) {
      setErrors((prev) => ({ ...prev, [field]: undefined }))
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="skill">Skill</Label>
        <Select value={formData.skill_name} onValueChange={(value: SkillName) => updateField("skill_name", value)}>
          <SelectTrigger>
            <SelectValue placeholder="Select a skill" />
          </SelectTrigger>
          <SelectContent>
            {SKILL_OPTIONS.map((skill) => (
              <SelectItem key={skill} value={skill}>
                {skill}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
        {errors.skill_name && <p className="text-sm text-red-500">{errors.skill_name}</p>}
      </div>

      <div className="space-y-2">
        <Label htmlFor="description">Description</Label>
        <Textarea
          id="description"
          placeholder="Describe your experience with this skill..."
          value={formData.description}
          onChange={(e) => updateField("description", e.target.value)}
          className={errors.description ? "border-red-500" : ""}
        />
        {errors.description && <p className="text-sm text-red-500">{errors.description}</p>}
      </div>

      <div className="space-y-2">
        <Label htmlFor="months">Experience (Months)</Label>
        <Input
            id="months"
            type="number"
            min="0"
            value={formData.months}
            onChange={(e) => {
                const rawValue = e.target.value;
                // Remove leading zeros
                const sanitizedValue = rawValue.replace(/^0+(?=\d)/, '');
                updateField("months", Number.parseInt(sanitizedValue) || 0);
            }}
        className={errors.months ? "border-red-500" : ""}
        />
        {errors.months && <p className="text-sm text-red-500">{errors.months}</p>}
      </div>

      <div className="space-y-2">
        <Label htmlFor="level">Level</Label>
        <Select value={formData.level} onValueChange={(value: SkillLevel) => updateField("level", value)}>
          <SelectTrigger>
            <SelectValue placeholder="Select level" />
          </SelectTrigger>
          <SelectContent>
            {LEVEL_OPTIONS.map((level) => (
              <SelectItem key={level} value={level}>
                {level === "CollegeResearch" ? "College Research" : level}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
        {errors.level && <p className="text-sm text-red-500">{errors.level}</p>}
      </div>

      <div className="flex justify-end space-x-2 pt-4">
        <Button type="button" variant="outline" onClick={onCancel}>
          Cancel
        </Button>
        <Button type="submit">Add Skill</Button>
      </div>
    </form>
  )
}
