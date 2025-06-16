'use client';
import AuthGuard from '../../components/AuthGuard';
import ObrasPage from './ObrasPage'; // ou como está organizado

export default function ObrasWrapper() {
  return (
    <AuthGuard>
      <ObrasPage />
    </AuthGuard>
  );
}
