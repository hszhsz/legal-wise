'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  ChevronRightIcon, 
  ShieldCheckIcon, 
  UserGroupIcon,
  ChatBubbleLeftRightIcon,
  DocumentTextIcon,
  MagnifyingGlassIcon,
  SparklesIcon
} from '@heroicons/react/24/outline'
import Link from 'next/link'
import RightifyLogo from '../components/RightifyLogo'

const features = [
  {
    name: '智能案情分析',
    description: '基于AI的深度案情分析，快速识别法律关键点和风险要素',
    icon: DocumentTextIcon,
    color: 'from-gray-800 to-gray-600'
  },
  {
    name: '精准案例检索',
    description: '海量法律案例数据库，智能匹配相似案例和判决先例',
    icon: MagnifyingGlassIcon,
    color: 'from-gray-700 to-gray-500'
  },
  {
    name: '专业律师推荐',
    description: '根据案件类型和地域，推荐最适合的专业律师',
    icon: UserGroupIcon,
    color: 'from-gray-900 to-gray-700'
  },
  {
    name: '实时法律咨询',
    description: '24/7在线法律咨询服务，即时获得专业法律建议',
    icon: ChatBubbleLeftRightIcon,
    color: 'from-black to-gray-800'
  }
]

const stats = [
  { name: '案例数据库', value: '100万+', description: '覆盖全国各级法院判决' },
  { name: '专业律师', value: '5000+', description: '认证执业律师入驻' },
  { name: '服务用户', value: '50万+', description: '累计服务用户数量' },
  { name: '咨询准确率', value: '95%+', description: 'AI法律分析准确率' }
]

const testimonials = [
  {
    content: "Rightify帮助我快速分析了合同纠纷的关键问题，节省了大量时间和成本。",
    author: "张先生",
    role: "企业法务",
    company: "某科技公司"
  },
  {
    content: "平台推荐的律师非常专业，成功帮助我解决了劳动争议问题。",
    author: "李女士",
    role: "个人用户",
    company: "某制造企业"
  },
  {
    content: "AI分析报告详细准确，为我的案件策略提供了重要参考。",
    author: "王律师",
    role: "执业律师",
    company: "某律师事务所"
  }
]

export default function HomePage() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="fixed w-full bg-white/95 backdrop-blur-sm border-b border-gray-300 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <div className="flex-shrink-0 flex items-center">
                <RightifyLogo size={32} className="text-gray-900" />
                <span className="ml-2 text-xl font-bold text-gray-900">Rightify</span>
              </div>
            </div>
            
            <div className="hidden md:block">
              <div className="ml-10 flex items-baseline space-x-4">
                <a href="#features" className="text-gray-600 hover:text-gray-900 px-3 py-2 text-sm font-medium transition-colors">
                  功能特色
                </a>
                <a href="#about" className="text-gray-600 hover:text-gray-900 px-3 py-2 text-sm font-medium transition-colors">
                  关于我们
                </a>
                <a href="#testimonials" className="text-gray-600 hover:text-gray-900 px-3 py-2 text-sm font-medium transition-colors">
                  用户评价
                </a>
                <Link href="/consultation" className="bg-gray-900 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-black transition-colors">
                  开始咨询
                </Link>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-20 pb-16 bg-gradient-to-br from-gray-100 via-white to-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
            >
              <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
                智能法律咨询
                <span className="block text-transparent bg-clip-text bg-gradient-to-r from-gray-900 to-black">
                  让公正触手可及
                </span>
              </h1>
              <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
                基于先进AI技术的法律咨询平台，提供案情分析、案例检索、律师推荐等一站式法律服务，
                让法律咨询更智能、更高效、更专业。
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link href="/consultation" className="inline-flex items-center px-8 py-3 border border-transparent text-base font-medium rounded-lg text-white bg-gray-900 hover:bg-black transition-colors">
                  立即体验
                  <ChevronRightIcon className="ml-2 h-5 w-5" />
                </Link>
                <button className="inline-flex items-center px-8 py-3 border border-gray-400 text-base font-medium rounded-lg text-gray-800 bg-white hover:bg-gray-100 transition-colors">
                  观看演示
                  <SparklesIcon className="ml-2 h-5 w-5" />
                </button>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <motion.div
                key={stat.name}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="text-center"
              >
                <div className="text-3xl md:text-4xl font-bold text-blue-600 mb-2">
                  {stat.value}
                </div>
                <div className="text-lg font-semibold text-gray-900 mb-1">
                  {stat.name}
                </div>
                <div className="text-sm text-gray-600">
                  {stat.description}
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              核心功能特色
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              融合人工智能与法律专业知识，为您提供全方位的智能法律服务
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={feature.name}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-shadow"
              >
                <div className="flex items-center mb-4">
                  <div className={`p-3 rounded-lg bg-gradient-to-r ${feature.color}`}>
                    <feature.icon className="h-6 w-6 text-white" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 ml-4">
                    {feature.name}
                  </h3>
                </div>
                <p className="text-gray-600 leading-relaxed">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* How it Works */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              工作流程
            </h2>
            <p className="text-xl text-gray-600">
              简单三步，获得专业法律建议
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                step: '01',
                title: '描述问题',
                description: '详细描述您的法律问题或案件情况'
              },
              {
                step: '02', 
                title: 'AI分析',
                description: '智能系统分析案情并制定解决方案'
              },
              {
                step: '03',
                title: '获得建议',
                description: '收到专业的法律建议和行动指南'
              }
            ].map((item, index) => (
              <motion.div
                key={item.step}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.2 }}
                className="text-center"
              >
                <div className="w-16 h-16 bg-blue-600 text-white rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-4">
                  {item.step}
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  {item.title}
                </h3>
                <p className="text-gray-600">
                  {item.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section id="testimonials" className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              用户评价
            </h2>
            <p className="text-xl text-gray-600">
              听听用户对我们服务的真实反馈
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="bg-white rounded-2xl p-6 shadow-lg"
              >
                <p className="text-gray-600 mb-4 italic">
                  "{testimonial.content}"
                </p>
                <div className="flex items-center">
                  <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                    <span className="text-blue-600 font-semibold">
                      {testimonial.author[0]}
                    </span>
                  </div>
                  <div className="ml-3">
                    <div className="text-sm font-semibold text-gray-900">
                      {testimonial.author}
                    </div>
                    <div className="text-xs text-gray-500">
                      {testimonial.role} · {testimonial.company}
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-gray-900 to-black">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
              准备开始您的法律咨询之旅？
            </h2>
            <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
              立即体验Rightify的智能法律服务，获得专业、高效的法律建议
            </p>
            <Link href="/consultation" className="inline-flex items-center px-8 py-3 border border-transparent text-base font-medium rounded-lg text-gray-900 bg-white hover:bg-gray-100 transition-colors">
              开始免费咨询
              <ChevronRightIcon className="ml-2 h-5 w-5" />
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="col-span-1 md:col-span-2">
              <div className="flex items-center mb-4">
                <RightifyLogo size={32} className="text-gray-400" />
                <span className="ml-2 text-xl font-bold">Rightify</span>
              </div>
              <p className="text-gray-400 mb-4">
                基于AI技术的智能法律咨询平台，致力于让法律服务更加智能化、便民化。
              </p>
              <div className="flex space-x-4">
                <ShieldCheckIcon className="h-5 w-5 text-gray-400" />
                <span className="text-sm text-gray-400">数据安全保护</span>
              </div>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold mb-4">服务</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">法律咨询</a></li>
                <li><a href="#" className="hover:text-white transition-colors">案例检索</a></li>
                <li><a href="#" className="hover:text-white transition-colors">律师推荐</a></li>
                <li><a href="#" className="hover:text-white transition-colors">文档分析</a></li>
              </ul>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold mb-4">联系我们</h3>
              <ul className="space-y-2 text-gray-400">
                <li>客服热线：400-123-4567</li>
                <li>邮箱：contact@legalwise.com</li>
                <li>地址：北京市朝阳区xxx大厦</li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2024 Rightify. 保留所有权利。</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
