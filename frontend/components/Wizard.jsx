// components/Wizard.jsx
'use client';

import { useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';

// Importação dos componentes de etapa (troque para os seus reais)
import Etapa1 from './Etapa1';
import Etapa2 from './Etapa2';
import Etapa3 from './Etapa3';

const steps = [
  { id: 0, component: <Etapa1 /> },
  { id: 1, component: <Etapa2 /> },
  { id: 2, component: <Etapa3 /> },
];

export default function Wizard() {
  const [currentStep, setCurrentStep] = useState(0);

  const nextStep = () => {
    if (currentStep < steps.length - 1) setCurrentStep(currentStep + 1);
  };

  const prevStep = () => {
    if (currentStep > 0) setCurrentStep(currentStep - 1);
  };

  return (
    <div className="w-full max-w-2xl mx-auto p-4 bg-white rounded-xl shadow-md">
      <AnimatePresence mode="wait">
        <motion.div
          key={currentStep}
          initial={{ opacity: 0, x: 100 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -100 }}
          transition={{ duration: 0.4 }}
        >
          {steps[currentStep].component}
        </motion.div>
      </AnimatePresence>

      <div className="flex justify-between mt-6">
        <button
          onClick={prevStep}
          disabled={currentStep === 0}
          className="px-4 py-2 bg-gray-200 rounded disabled:opacity-50"
        >
          Voltar
        </button>
        <button
          onClick={nextStep}
          disabled={currentStep === steps.length - 1}
          className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50"
        >
          Avançar
        </button>
      </div>
    </div>
  );
}
