import React from 'react';
import ModelSelector from './ModelSelector';
import ParameterSlider from './ParameterSlider';
import { useMutation } from 'react-query';
import { updateConfig } from '../../services/api';

function Config() {
  const configMutation = useMutation(updateConfig, {
    onSuccess: () => {
      // TODO: Add success notification
      console.log('Configuration updated successfully');
    },
    onError: (error) => {
      // TODO: Add error notification
      console.error('Configuration update failed:', error);
    }
  });

  const handleConfigUpdate = (key, value) => {
    configMutation.mutate({ [key]: value });
  };

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-6">Model Configuration</h2>
      
      <div className="space-y-6">
        <ModelSelector 
          onChange={(model) => handleConfigUpdate('model', model)}
          options={[
            { value: 'gpt-3.5-turbo', label: 'GPT-3.5 Turbo' },
            { value: 'gpt-4', label: 'GPT-4' },
            { value: 'claude-2', label: 'Claude 2' }
          ]}
        />

        <div className="grid gap-6 md:grid-cols-2">
          <ParameterSlider
            label="Temperature"
            value={0.7}
            min={0}
            max={1}
            step={0.1}
            onChange={(value) => handleConfigUpdate('temperature', value)}
            tooltip="Controls randomness in responses. Higher values make output more creative but less focused."
          />

          <ParameterSlider
            label="Max Tokens"
            value={1000}
            min={100}
            max={4000}
            step={100}
            onChange={(value) => handleConfigUpdate('max_tokens', value)}
            tooltip="Maximum length of the generated response."
          />

          <ParameterSlider
            label="Top P"
            value={0.9}
            min={0}
            max={1}
            step={0.1}
            onChange={(value) => handleConfigUpdate('top_p', value)}
            tooltip="Controls diversity via nucleus sampling. Lower values make output more focused."
          />

          <ParameterSlider
            label="Frequency Penalty"
            value={0}
            min={0}
            max={2}
            step={0.1}
            onChange={(value) => handleConfigUpdate('frequency_penalty', value)}
            tooltip="Reduces repetition by lowering the likelihood of repeated tokens."
          />
        </div>
      </div>
    </div>
  );
}

export default Config; 