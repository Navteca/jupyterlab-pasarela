import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { requestAPI } from '../handler';

const getUsage = async () => await requestAPI<any>('usage');

/**
 * React component for a counter.
 *
 * @returns The React component
 */
export const PasarelaHelpComponent: React.FC = () => {
  const [content, setContent] = useState<string>('');
  useEffect(() => {
    getUsage()
      .then(setContent)
      .catch(e => {
        console.log(e);
      });
  }, []);

  return (
    <div className="container">
      <ReactMarkdown
        children={content}
        remarkPlugins={[remarkGfm]}
      ></ReactMarkdown>
    </div>
  );
};
