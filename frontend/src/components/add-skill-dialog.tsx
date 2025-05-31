"use client"

import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { SkillForm } from "./skill-form"
import type { SkillFormData } from "@/types/skill"

interface AddSkillDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onAddSkill: (data: SkillFormData) => void
}

export function AddSkillDialog({ open, onOpenChange, onAddSkill }: AddSkillDialogProps) {
  const handleSubmit = (data: SkillFormData) => {
    onAddSkill(data)
    onOpenChange(false)
  }

  const handleCancel = () => {
    onOpenChange(false)
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Add New Skill</DialogTitle>
          <DialogDescription>
            Add a new skill to your profile. Fill in all the details about your experience.
          </DialogDescription>
        </DialogHeader>
        <SkillForm onSubmit={handleSubmit} onCancel={handleCancel} />
      </DialogContent>
    </Dialog>
  )
}
