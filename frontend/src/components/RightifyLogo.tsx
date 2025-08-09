import React from 'react';

interface RightifyLogoProps {
  size?: number;
  className?: string;
}

const RightifyLogo: React.FC<RightifyLogoProps> = ({ 
  size = 32, 
  className = "" 
}) => {
  return (
    <svg 
      width={size} 
      height={size} 
      viewBox="0 0 32 32" 
      fill="none" 
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      {/* 主体圆形 - 简约现代 */}
      <circle 
        cx="16" 
        cy="16" 
        r="15" 
        fill="currentColor"
        opacity="0.1"
      />
      
      {/* 核心天平图标 - 极简设计 */}
      <g transform="translate(16, 16)">
        {/* 天平横梁 */}
        <line 
          x1="-8" 
          y1="-2" 
          x2="8" 
          y2="-2" 
          stroke="currentColor" 
          strokeWidth="2.5"
          strokeLinecap="round"
        />
        
        {/* 左侧天平盘 */}
        <path 
          d="M-8 -2 L-10 2 L-6 2 Z" 
          fill="currentColor"
        />
        
        {/* 右侧天平盘 */}
        <path 
          d="M8 -2 L6 2 L10 2 Z" 
          fill="currentColor"
        />
        
        {/* 中央支柱 */}
        <line 
          x1="0" 
          y1="-2" 
          x2="0" 
          y2="6" 
          stroke="currentColor" 
          strokeWidth="2.5"
          strokeLinecap="round"
        />
        
        {/* 底座 */}
        <line 
          x1="-3" 
          y1="6" 
          x2="3" 
          y2="6" 
          stroke="currentColor" 
          strokeWidth="2.5"
          strokeLinecap="round"
        />
      </g>
    </svg>
  );
};

export default RightifyLogo;