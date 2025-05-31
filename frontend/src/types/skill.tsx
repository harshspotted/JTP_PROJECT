export type SkillName =
  | "Python"
  | "AI and Machine learning"
  | "Git"
  | "MongoDB"
  | "SQL"
  | "Docker"
  | "Excel"
  | "Javascript"
  | "Cloud Platform"

export type SkillLevel = "Basic" | "CollegeResearch" | "Professional" | "Other"

export interface Skill {
  id: string
  skill_name: SkillName
  level: SkillLevel
  months: number
  description?: string
}

export interface SkillFormData {
  skill_name: SkillName
  level: SkillLevel
  months: number
  description: string
}

export interface SkillMetadata {
  skill_name: SkillName
  level: SkillLevel
  months: number
}

export interface RecommendationRequest {
  skills: Skill[]
  description: string
  top_k: number
}

export interface RecommendationWithMetaDataResult {
  rank: number
  project_id: string
  score: number
  description: string
  required_skills: SkillMetadata[]
}

// Analysis types
export interface AnalysisRequest {
  employee_skills: SkillMetadata[]
  employee_description: string
  project_skills: SkillMetadata[]
  project_description: string
  score: number
}

export interface AnalysisResult {
  fitness_evaluation: string
  recommended_courses: string
}


// const mockRecommendations: RecommendationWithMetaDataResult[] = [
//     {
//     rank: 1,
//     project_id: "proj_001",
//     score: 0.95,
//     description:
//         "Build a full-stack e-commerce platform with React, Node.js, and MongoDB. Implement user authentication, payment processing, and inventory management.",
//     required_skills: [
//         { skill_name: "Javascript", level: "Professional", months: 24 },
//         { skill_name: "MongoDB", level: "Professional", months: 18 },
//         { skill_name: "Git", level: "Professional", months: 12 },
//     ],
//     },
//     {
//     rank: 2,
//     project_id: "proj_002",
//     score: 0.87,
//     description:
//         "Create a machine learning model for predictive analytics using Python and deploy it using Docker containers on cloud platforms.",
//     required_skills: [
//         { skill_name: "Python", level: "Professional", months: 36 },
//         { skill_name: "AI and Machine learning", level: "Professional", months: 24 },
//         { skill_name: "Docker", level: "CollegeResearch", months: 12 },
//         { skill_name: "Cloud Platform", level: "Professional", months: 18 },
//     ],
//     },
// ]
