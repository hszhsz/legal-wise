'use client'

import { useState, useRef, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { motion } from 'framer-motion'
import {
  PaperAirplaneIcon,
  DocumentTextIcon,
  MagnifyingGlassIcon,
  UserGroupIcon,
  ChartBarIcon,
  ArrowLeftIcon,
  SparklesIcon
} from '@heroicons/react/24/outline'
import { ArrowLeft, Send, MessageCircle, BarChart3, Search, FileText, MessageSquare } from 'lucide-react'
import Link from 'next/link'

interface Message {
  id: string
  type: 'user' | 'assistant'
  content: string
  timestamp: Date
}

interface ServiceOption {
  id: string
  name: string
  description: string
  icon: any
  endpoint: string
  color: string
}

const services: ServiceOption[] = [
  {
    id: 'consult',
    name: '法律咨询',
    description: '获得专业的法律建议和解答',
    icon: DocumentTextIcon,
    endpoint: '/api/legal/consult',
    color: 'from-gray-800 to-gray-600'
  },
  {
    id: 'analyze',
    name: '案情分析',
    description: '深度分析案件情况和法律要点',
    icon: ChartBarIcon,
    endpoint: '/api/legal/analyze',
    color: 'from-gray-900 to-gray-700'
  },
  {
    id: 'search',
    name: '案例检索',
    description: '查找相关法律案例和判决先例',
    icon: MagnifyingGlassIcon,
    endpoint: '/api/legal/search-cases',
    color: 'from-black to-gray-800'
  },
  {
    id: 'recommend',
    name: '律师推荐',
    description: '推荐专业对口的执业律师',
    icon: UserGroupIcon,
    endpoint: '/api/legal/recommend-lawyers',
    color: 'from-gray-700 to-gray-500'
  }
]

interface AgentAction {
  id: string
  type: string
  content: string
  timestamp: Date
  data?: any
  isStreaming?: boolean
}

interface FinalReport {
  title: string
  content: string
  sections: Array<{
    title: string
    content: string
  }>
}

const formatTime = (date: Date) => {
  return date.toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 打字机效果组件
const TypewriterText = ({ text, speed = 50 }: { text: string; speed?: number }) => {
  const [displayText, setDisplayText] = useState('')
  const [currentIndex, setCurrentIndex] = useState(0)

  useEffect(() => {
    if (currentIndex < text.length) {
      const timer = setTimeout(() => {
        setDisplayText(prev => prev + text[currentIndex])
        setCurrentIndex(prev => prev + 1)
      }, speed)
      return () => clearTimeout(timer)
    }
  }, [currentIndex, text, speed])

  useEffect(() => {
    setDisplayText('')
    setCurrentIndex(0)
  }, [text])

  return <span>{displayText}</span>
}

export default function ConsultationPage() {
  const router = useRouter()
  const [messages, setMessages] = useState<Message[]>([])
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [selectedService, setSelectedService] = useState<ServiceOption | null>(null)
  const [agentActions, setAgentActions] = useState<AgentAction[]>([])
  const [finalReport, setFinalReport] = useState<FinalReport | null>(null)
  const [showChatHistory, setShowChatHistory] = useState(false)
  const [showAgentActions, setShowAgentActions] = useState(true)
  const [showServiceSelection, setShowServiceSelection] = useState(true)
  const [streamingActionContent, setStreamingActionContent] = useState<{[key: string]: string}>({})
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)
  const actionsEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const scrollActionsToBottom = () => {
    actionsEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    scrollActionsToBottom()
  }, [agentActions])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!inputValue.trim() || !selectedService) return

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: inputValue,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputValue('')
    setIsLoading(true)
    setFinalReport(null)
    console.log('Clearing agentActions')
    setAgentActions([])
    console.log('AgentActions cleared, starting consultation...')
    setShowAgentActions(true)
    setShowServiceSelection(false)
    setStreamingActionContent({})

    try {
      const response = await fetch(`http://localhost:8001${selectedService.endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: inputValue })
      })

      if (!response.ok) {
        throw new Error('Network response was not ok')
      }

      const reader = response.body?.getReader()
      const decoder = new TextDecoder()
      let assistantMessage = ''
      
      const assistantMessageId = (Date.now() + 1).toString()
      setMessages(prev => [...prev, {
        id: assistantMessageId,
        type: 'assistant',
        content: '',
        timestamp: new Date()
      }])

      if (reader) {
        while (true) {
          const { done, value } = await reader.read()
          if (done) break
          
          const chunk = decoder.decode(value)
          const lines = chunk.split('\n')
          
          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const data = line.slice(6).trim()
              if (data === '[DONE]' || data === '' || data.startsWith('data: ')) {
                continue
              }
              try {
                const parsed = JSON.parse(data)
                console.log('Successfully parsed SSE data:', parsed)
                
                // Add to agent actions for real-time display
                const newAction: AgentAction = {
                  id: Date.now().toString() + Math.random(),
                  type: parsed.type || 'unknown',
                  content: parsed.content || '',
                  timestamp: new Date(),
                  data: parsed.data,
                  isStreaming: true
                }
                
                console.log('Adding new action:', newAction)
                setAgentActions(prev => {
                  const updated = [...prev, newAction]
                  console.log('Updated agentActions:', updated)
                  return updated
                })
                
                // 设置延时后停止流式效果
                setTimeout(() => {
                  setAgentActions(prevActions => 
                    prevActions.map(action => 
                      action.id === newAction.id 
                        ? { ...action, isStreaming: false }
                        : action
                    )
                  )
                }, Math.max(1000, (parsed.content || '').length * 30))
                
                // Handle different event types
                switch (parsed.type) {
                  case 'final_answer':
                    // Parse final answer as report
                    const reportSections = parsed.content.split('\n\n').filter((section: string) => section.trim())
                     setFinalReport({
                       title: '法律咨询分析报告',
                       content: parsed.content,
                       sections: reportSections.map((section: string, index: number) => ({
                         title: `第${index + 1}部分`,
                         content: section
                       }))
                     })
                    
                    // Also add to chat messages
                    assistantMessage = `📝 **分析完成** - 详细报告请查看右侧面板\n\n${parsed.content}`
                    setMessages(prev => prev.map(msg => 
                      msg.id === assistantMessageId 
                        ? { ...msg, content: assistantMessage }
                        : msg
                    ))
                    break
                  
                  case 'complete':
                    // Don't add complete message to chat, just update loading state
                    break
                  
                  case 'error':
                    assistantMessage += `❌ 错误：${parsed.content}\n\n`
                    setMessages(prev => prev.map(msg => 
                      msg.id === assistantMessageId 
                        ? { ...msg, content: assistantMessage }
                        : msg
                    ))
                    break
                  
                  default:
                    // For other types, just show brief status in chat
                    if (parsed.type === 'start') {
                      assistantMessage = '🚀 开始分析您的法律问题...'
                    } else if (parsed.type === 'planning') {
                      assistantMessage += '📋 制定执行计划...\n'
                    } else if (parsed.type === 'execution') {
                      assistantMessage += `⚙️ ${parsed.content}\n`
                    }
                    
                    setMessages(prev => prev.map(msg => 
                      msg.id === assistantMessageId 
                        ? { ...msg, content: assistantMessage }
                        : msg
                    ))
                    break
                }
              } catch (e) {
                // Ignore parsing errors for incomplete JSON
                console.warn('Failed to parse SSE data:', data, e)
                console.log('Raw line:', line)
                console.log('Extracted data:', data)
                console.log('Data length:', data.length)
                console.log('Data starts with:', data.substring(0, 50))
              }
            }
          }
        }
      }
    } catch (error) {
      console.error('Error:', error)
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: '抱歉，服务暂时不可用。请稍后再试。',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e as any)
    }
  }



  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4">
              <Link href="/" className="flex items-center text-gray-600 hover:text-gray-900 transition-colors">
                <ArrowLeftIcon className="h-5 w-5 mr-2" />
                返回首页
              </Link>
              <button
                onClick={() => setShowChatHistory(!showChatHistory)}
                className="flex items-center px-3 py-2 text-sm bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-100"
              >
                <DocumentTextIcon className="w-4 h-4 mr-2" />
                {showChatHistory ? '隐藏' : '显示'}聊天记录
              </button>
              {!showServiceSelection && selectedService && (
                <button
                  onClick={() => setShowServiceSelection(true)}
                  className="flex items-center px-3 py-2 text-sm bg-green-50 text-green-600 rounded-lg hover:bg-green-100"
                >
                  <ChartBarIcon className="w-4 h-4 mr-2" />
                  切换服务
                </button>
              )}
            </div>
            <h1 className="text-xl font-semibold text-gray-900">Rightify 智能咨询</h1>
            <div className="w-32"></div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className={`grid grid-cols-1 gap-8 ${
          showChatHistory && showAgentActions && showServiceSelection ? 'lg:grid-cols-12' :
          (showChatHistory && showAgentActions) || (showChatHistory && showServiceSelection) || (showAgentActions && showServiceSelection) ? 'lg:grid-cols-9' :
          showChatHistory || showAgentActions ? 'lg:grid-cols-6' :
          showServiceSelection ? 'lg:grid-cols-12' :
          'lg:grid-cols-3'
        }`}>
          {/* Chat History Sidebar */}
          {showChatHistory && (
            <div className="lg:col-span-3">
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 h-[calc(100vh-200px)]">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">聊天记录</h2>
                <div className="space-y-3 overflow-y-auto">
                  {messages.map((message) => (
                    <div key={message.id} className="p-3 rounded-lg bg-gray-50">
                      <div className="text-sm font-medium text-gray-900 mb-1">
                        {message.type === 'user' ? '用户' : 'AI助手'}
                      </div>
                      <div className="text-sm text-gray-600 line-clamp-3">
                        {message.content}
                      </div>
                      <div className="text-xs text-gray-400 mt-1">
                        {formatTime(message.timestamp)}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Service Selection Sidebar */}
          {showServiceSelection && (
            <div className={`${
              showChatHistory && showAgentActions ? 'lg:col-span-2' :
              showChatHistory || showAgentActions ? 'lg:col-span-3' :
              'lg:col-span-3'
            }`}>
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">选择服务类型</h2>
              <div className="space-y-3">
                {services.map((service) => (
                  <motion.button
                    key={service.id}
                    onClick={() => setSelectedService(service)}
                    className={`w-full text-left p-4 rounded-lg border-2 transition-all ${
                      selectedService?.id === service.id
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-200 hover:border-gray-300 bg-white'
                    }`}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                  >
                    <div className="flex items-center mb-2">
                      <div className={`p-2 rounded-lg bg-gradient-to-r ${service.color} mr-3`}>
                        <service.icon className="h-5 w-5 text-white" />
                      </div>
                      <h3 className="font-medium text-gray-900">{service.name}</h3>
                    </div>
                    <p className="text-sm text-gray-600">{service.description}</p>
                  </motion.button>
                ))}
              </div>
            </div>
            </div>
          )}

          {/* Chat Interface */}
          <div className={`${
            showChatHistory && showAgentActions && showServiceSelection ? 'lg:col-span-4' :
            showChatHistory && showAgentActions ? 'lg:col-span-3' :
            (showChatHistory && showServiceSelection) || (showAgentActions && showServiceSelection) ? 'lg:col-span-3' :
            showChatHistory || showAgentActions ? 'lg:col-span-3' :
            showServiceSelection ? 'lg:col-span-9' :
            'lg:col-span-3'
          }`}>
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 h-[calc(100vh-200px)] flex flex-col">
              {/* Chat Header */}
              <div className="p-6 border-b border-gray-200">
                <div className="flex items-center">
                  <SparklesIcon className="h-6 w-6 text-blue-600 mr-2" />
                  <h2 className="text-lg font-semibold text-gray-900">
                    {selectedService ? selectedService.name : '请选择服务类型'}
                  </h2>
                </div>
                {selectedService && (
                  <p className="text-sm text-gray-600 mt-1">{selectedService.description}</p>
                )}
              </div>

              {/* Messages */}
              <div className="flex-1 overflow-y-auto p-6 space-y-4">
                {messages.length === 0 && (
                  <div className="text-center py-12">
                    <SparklesIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-gray-900 mb-2">开始您的法律咨询</h3>
                    <p className="text-gray-600">
                      {selectedService 
                        ? `描述您的${selectedService.name}需求，我将为您提供专业建议`
                        : '请先选择一个服务类型，然后开始咨询'
                      }
                    </p>
                  </div>
                )}
                
                {messages.map((message) => (
                  <motion.div
                    key={message.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div className={`max-w-3xl px-4 py-3 rounded-lg ${
                      message.type === 'user'
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-100 text-gray-900'
                    }`}>
                      <div className="whitespace-pre-wrap">{message.content}</div>
                      <div className={`text-xs mt-2 ${
                        message.type === 'user' ? 'text-blue-100' : 'text-gray-500'
                      }`}>
                        {formatTime(message.timestamp)}
                      </div>
                    </div>
                  </motion.div>
                ))}
                
                {isLoading && (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="flex justify-start"
                  >
                    <div className="bg-gray-100 text-gray-900 px-4 py-3 rounded-lg">
                      <div className="flex items-center space-x-2">
                        <div className="flex space-x-1">
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                        </div>
                        <span className="text-sm text-gray-600">正在分析...</span>
                      </div>
                    </div>
                  </motion.div>
                )}
                <div ref={messagesEndRef} />
              </div>

              {/* Input Form */}
              <div className="p-6 border-t border-gray-200">
                <form onSubmit={handleSubmit} className="flex space-x-4">
                  <div className="flex-1">
                    <textarea
                      ref={textareaRef}
                      value={inputValue}
                      onChange={(e) => setInputValue(e.target.value)}
                      onKeyPress={handleKeyPress}
                      placeholder={selectedService ? `请描述您的${selectedService.name}需求...` : '请先选择服务类型'}
                      disabled={!selectedService || isLoading}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none disabled:bg-gray-100 disabled:cursor-not-allowed text-gray-900 placeholder:text-gray-500"
                      rows={3}
                    />
                  </div>
                  <button
                    type="submit"
                    disabled={!inputValue.trim() || !selectedService || isLoading}
                    className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors flex items-center"
                  >
                    <PaperAirplaneIcon className="h-5 w-5" />
                  </button>
                </form>
                <p className="text-xs text-gray-500 mt-2">
                  按 Enter 发送，Shift + Enter 换行
                </p>
              </div>
            </div>
          </div>

          {/* Agent Actions Panel */}
          {showAgentActions && (
            <div className={`${
              showChatHistory && showServiceSelection ? 'lg:col-span-3' :
              showChatHistory || showServiceSelection ? 'lg:col-span-3' :
              'lg:col-span-3'
            }`}>
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 h-[calc(100vh-200px)] flex flex-col">
                <div className="p-6 border-b border-gray-200">
                  <h2 className="text-lg font-semibold text-gray-900">AI 执行过程</h2>
                  <p className="text-sm text-gray-600 mt-1">实时查看AI分析步骤</p>
                </div>
                
                <div className="flex-1 overflow-y-auto p-6 space-y-4">
                  {agentActions.length === 0 ? (
                    <div className="text-center py-12">
                      <SparklesIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                      <p className="text-gray-600">等待AI开始分析...</p>
                    </div>
                  ) : (
                    agentActions.map((action) => (
                      <motion.div
                        key={action.id}
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        className="p-4 rounded-lg bg-gray-50 border-l-4 border-blue-500"
                      >
                        <div className="flex items-center mb-2">
                          <div className="w-2 h-2 bg-blue-500 rounded-full mr-2"></div>
                          <span className="text-sm font-medium text-gray-900">
                            {action.type === 'start' && '开始分析'}
                            {action.type === 'planning' && '制定计划'}
                            {action.type === 'execution' && '执行步骤'}
                            {action.type === 'final_answer' && '生成报告'}
                            {action.type === 'complete' && '分析完成'}
                            {action.type === 'error' && '错误'}
                            {!['start', 'planning', 'execution', 'final_answer', 'complete', 'error'].includes(action.type) && action.type}
                          </span>
                          <span className="text-xs text-gray-500 ml-auto">
                            {formatTime(action.timestamp)}
                          </span>
                        </div>
                        <div className="text-sm text-gray-700">
                          {action.isStreaming ? (
                            <TypewriterText text={action.content} speed={30} />
                          ) : (
                            action.content
                          )}
                        </div>
                      </motion.div>
                    ))
                  )}
                  <div ref={actionsEndRef} />
                </div>
                
                {finalReport && (
                  <div className="p-6 border-t border-gray-200">
                    <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                      <div className="flex items-center mb-2">
                        <DocumentTextIcon className="h-5 w-5 text-green-600 mr-2" />
                        <span className="text-sm font-medium text-green-800">分析报告已生成</span>
                      </div>
                      <p className="text-sm text-green-700">
                        详细的法律分析报告已完成，请查看聊天界面获取完整内容。
                      </p>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}