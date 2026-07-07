import { Bot } from "lucide-react"
import { Link } from "react-router-dom"


export const Logo = () => {
  return (
     <Link to="/" className="flex items-center gap-2 text-xl font-bold">
          <div className="rounded-md bg-gradient-to-r from-[#5133CA] to-[#B72CFF] p-2">
            <Bot size={24} />
          </div>
          <span>InterviewAI</span>
        </Link>
  )
}
