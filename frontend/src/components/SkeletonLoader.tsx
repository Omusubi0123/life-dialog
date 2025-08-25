/**
 * スケルトンローディングコンポーネント
 */

import React from 'react';

const SkeletonLoader: React.FC = () => {
  return (
    <div className="animate-pulse">
      {/* ナビゲーション部分 */}
      <div className="fixed top-0 left-0 w-full h-20 bg-gray-200"></div>
      
      {/* メインコンテンツ */}
      <div className="mt-24 mb-20 mx-10">
        {/* アコーディオン部分 */}
        <div className="space-y-4 mb-6">
          <div className="h-12 bg-gray-200 rounded"></div>
          <div className="h-8 bg-gray-200 rounded w-3/4"></div>
        </div>
        
        {/* タイムライン部分 */}
        <div className="space-y-6">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="flex space-x-4">
              <div className="w-12 h-12 bg-gray-200 rounded-full"></div>
              <div className="flex-1 space-y-2">
                <div className="h-4 bg-gray-200 rounded w-1/4"></div>
                <div className="h-16 bg-gray-200 rounded"></div>
              </div>
            </div>
          ))}
        </div>
      </div>
      
      {/* フッター部分 */}
      <div className="fixed bottom-0 left-0 w-full h-16 bg-gray-200"></div>
    </div>
  );
};

export default SkeletonLoader;
