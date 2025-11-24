# 🔗 Guia de Integração - Frontend + Backend

## 📱 Frontend → Backend Integration

### 1. Configuração Inicial

O Frontend (Next.js) precisa conhecer as URLs dos endpoints Lambda.

**Arquivo: `portfolio-site/.env.local`**

```env
NEXT_PUBLIC_API_BASE_URL=https://your-api-gateway-id.execute-api.us-east-1.amazonaws.com/prod
NEXT_PUBLIC_STRAVA_CLIENT_ID=seu_client_id
NEXT_PUBLIC_STRAVA_REDIRECT_URI=https://yourdomain.com/auth/callback
```

---

### 2. Auth Flow - Step by Step

#### 2.1 Frontend - Botão "Connect with Strava"

```typescript
// portfolio-site/app/components/StravaConnect.tsx

import { useRouter } from 'next/navigation';

export const StravaConnect = () => {
  const router = useRouter();
  
  const handleConnect = () => {
    const params = new URLSearchParams({
      client_id: process.env.NEXT_PUBLIC_STRAVA_CLIENT_ID!,
      redirect_uri: process.env.NEXT_PUBLIC_STRAVA_REDIRECT_URI!,
      response_type: 'code',
      scope: 'read,activity:read_all',
      approval_prompt: 'force' // Force re-authorization
    });
    
    window.location.href = 
      `https://www.strava.com/oauth/authorize?${params.toString()}`;
  };
  
  return (
    <button 
      onClick={handleConnect}
      className="bg-orange-600 hover:bg-orange-700 text-white px-6 py-2 rounded"
    >
      🚴 Connect with Strava
    </button>
  );
};
```

#### 2.2 Callback Handler

```typescript
// portfolio-site/app/auth/callback/page.tsx

'use client';

import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';

export default function AuthCallback() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [error, setError] = useState<string>('');
  
  useEffect(() => {
    const code = searchParams.get('code');
    const scope = searchParams.get('scope');
    
    if (!code) {
      setError('No authorization code received');
      setTimeout(() => router.push('/'), 3000);
      return;
    }
    
    // Enviar código para Lambda backend
    fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/auth/callback`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code, scope })
    })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          // Salvar token no localStorage
          localStorage.setItem('strava_token', data.data.access_token);
          localStorage.setItem('user_id', data.data.user_id);
          localStorage.setItem('athlete_name', data.data.athlete_name);
          
          // Redirecionar para dashboard
          router.push('/dashboard');
        } else {
          setError(data.error.message);
        }
      })
      .catch(err => {
        setError(err.message);
      });
  }, [searchParams, router]);
  
  return (
    <div className="flex items-center justify-center min-h-screen">
      {error ? (
        <div className="text-center">
          <h2 className="text-2xl font-bold text-red-600">Error</h2>
          <p className="text-gray-600">{error}</p>
          <p>Redirecting...</p>
        </div>
      ) : (
        <div className="text-center">
          <h2 className="text-2xl font-bold">Connecting...</h2>
          <p>Please wait while we connect your Strava account</p>
        </div>
      )}
    </div>
  );
}
```

---

### 3. Chamadas de API

#### 3.1 API Client Utility

```typescript
// portfolio-site/lib/api-client.ts

class StravaApiClient {
  private baseUrl: string;
  
  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL!;
  }
  
  private async request(
    endpoint: string,
    options?: RequestInit
  ) {
    const url = `${this.baseUrl}${endpoint}`;
    const token = typeof window !== 'undefined' 
      ? localStorage.getItem('strava_token')
      : null;
    
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options?.headers,
    };
    
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    
    const response = await fetch(url, {
      ...options,
      headers,
    });
    
    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`);
    }
    
    return response.json();
  }
  
  async getAthlete(userId: string, detailed = false) {
    return this.request(
      `/athlete/${userId}?detailed=${detailed}`
    );
  }
  
  async getActivities(
    userId: string,
    page = 1,
    perPage = 20,
    sportType?: string
  ) {
    const params = new URLSearchParams({
      page: String(page),
      per_page: String(perPage),
      ...(sportType && { sport_type: sportType }),
    });
    
    return this.request(
      `/activities/${userId}?${params.toString()}`
    );
  }
  
  async getStats(
    userId: string,
    period = 'month',
    sportType?: string
  ) {
    const params = new URLSearchParams({
      period,
      ...(sportType && { sport_type: sportType }),
    });
    
    return this.request(
      `/stats/${userId}?${params.toString()}`
    );
  }
  
  async getInsights(
    userId: string,
    type = 'all',
    days = 30
  ) {
    const params = new URLSearchParams({
      type,
      days: String(days),
    });
    
    return this.request(
      `/insights/${userId}?${params.toString()}`
    );
  }
}

export const apiClient = new StravaApiClient();
```

#### 3.2 React Hook para Dados

```typescript
// portfolio-site/lib/hooks/useStravaData.ts

import { useEffect, useState } from 'react';
import { apiClient } from '../api-client';

export function useAthlete(userId: string | null) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  useEffect(() => {
    if (!userId) return;
    
    setLoading(true);
    apiClient
      .getAthlete(userId, true)
      .then(res => {
        if (res.success) {
          setData(res.data.athlete);
        } else {
          setError(res.error.message);
        }
      })
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, [userId]);
  
  return { data, loading, error };
}

export function useActivities(
  userId: string | null,
  page = 1,
  sportType?: string
) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  useEffect(() => {
    if (!userId) return;
    
    setLoading(true);
    apiClient
      .getActivities(userId, page, 20, sportType)
      .then(res => {
        if (res.success) {
          setData(res.data);
        } else {
          setError(res.error.message);
        }
      })
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, [userId, page, sportType]);
  
  return { data, loading, error };
}

export function useStats(
  userId: string | null,
  period = 'month'
) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  useEffect(() => {
    if (!userId) return;
    
    setLoading(true);
    apiClient
      .getStats(userId, period)
      .then(res => {
        if (res.success) {
          setData(res.data.stats);
        } else {
          setError(res.error.message);
        }
      })
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, [userId, period]);
  
  return { data, loading, error };
}

export function useInsights(
  userId: string | null,
  days = 30
) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  useEffect(() => {
    if (!userId) return;
    
    setLoading(true);
    apiClient
      .getInsights(userId, 'all', days)
      .then(res => {
        if (res.success) {
          setData(res.data.insights);
        } else {
          setError(res.error.message);
        }
      })
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, [userId, days]);
  
  return { data, loading, error };
}
```

---

### 4. Dashboard Component

```typescript
// portfolio-site/app/dashboard/page.tsx

'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import {
  useAthlete,
  useActivities,
  useStats,
  useInsights
} from '@/lib/hooks/useStravaData';

export default function Dashboard() {
  const router = useRouter();
  const [userId, setUserId] = useState<string | null>(null);
  const [period, setPeriod] = useState('month');
  
  // Hooks
  const athlete = useAthlete(userId);
  const activities = useActivities(userId);
  const stats = useStats(userId, period);
  const insights = useInsights(userId);
  
  useEffect(() => {
    // Recuperar user_id do localStorage
    const id = localStorage.getItem('user_id');
    if (!id) {
      router.push('/');
      return;
    }
    setUserId(id);
  }, [router]);
  
  if (!userId) {
    return <div>Loading...</div>;
  }
  
  return (
    <div className="container mx-auto p-4">
      {/* Perfil */}
      {athlete.data && (
        <div className="mb-8">
          <h1 className="text-4xl font-bold">
            {athlete.data.firstname} {athlete.data.lastname}
          </h1>
          <p className="text-gray-600">{athlete.data.email}</p>
          {athlete.data.profile && (
            <img 
              src={athlete.data.profile}
              alt="Profile"
              className="w-32 h-32 rounded-full mt-4"
            />
          )}
        </div>
      )}
      
      {/* Estatísticas */}
      {stats.data && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white p-4 rounded shadow">
            <h3 className="text-gray-600">Total Activities</h3>
            <p className="text-2xl font-bold">
              {stats.data.total_activities}
            </p>
          </div>
          
          <div className="bg-white p-4 rounded shadow">
            <h3 className="text-gray-600">Total Distance</h3>
            <p className="text-2xl font-bold">
              {stats.data.total_distance} km
            </p>
          </div>
          
          <div className="bg-white p-4 rounded shadow">
            <h3 className="text-gray-600">Avg Speed</h3>
            <p className="text-2xl font-bold">
              {stats.data.average_speed} km/h
            </p>
          </div>
          
          <div className="bg-white p-4 rounded shadow">
            <h3 className="text-gray-600">Elevation Gain</h3>
            <p className="text-2xl font-bold">
              {stats.data.total_elevation_gain} m
            </p>
          </div>
        </div>
      )}
      
      {/* Atividades Recentes */}
      {activities.data && (
        <div className="bg-white p-4 rounded shadow">
          <h2 className="text-2xl font-bold mb-4">Recent Activities</h2>
          <div className="space-y-2">
            {activities.data.activities.map((activity: any) => (
              <div key={activity.id} className="border-b pb-2">
                <h3 className="font-semibold">{activity.name}</h3>
                <p className="text-sm text-gray-600">
                  {activity.distance}m · {activity.moving_time}s
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
      
      {/* Insights */}
      {insights.data && insights.data.recommendations && (
        <div className="bg-blue-50 p-4 rounded mt-8">
          <h2 className="text-2xl font-bold mb-4">Recommendations</h2>
          <div className="space-y-2">
            {insights.data.recommendations.suggestions.map(
              (rec: any, idx: number) => (
                <div key={idx} className="bg-white p-3 rounded">
                  <p className="font-semibold">{rec.message}</p>
                  <p className="text-sm text-gray-600">
                    {rec.recommendation}
                  </p>
                </div>
              )
            )}
          </div>
        </div>
      )}
    </div>
  );
}
```

---

### 5. Error Handling & Loading States

```typescript
// portfolio-site/app/components/DataDisplay.tsx

interface DataDisplayProps {
  data: any;
  loading: boolean;
  error: string | null;
  fallback?: React.ReactNode;
}

export const DataDisplay: React.FC<DataDisplayProps> = ({
  data,
  loading,
  error,
  fallback
}) => {
  if (loading) {
    return (
      <div className="flex justify-center items-center p-8">
        <div className="animate-spin">⏳</div>
        <span className="ml-2">Loading...</span>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 p-4 rounded">
        <p className="text-red-800 font-semibold">Error</p>
        <p className="text-red-600">{error}</p>
      </div>
    );
  }
  
  if (!data) {
    return fallback || <p>No data available</p>;
  }
  
  return <>{data}</>;
};
```

---

### 6. Environment Setup

**Arquivo: `.env.local` (Frontend)**

```env
# Strava OAuth
NEXT_PUBLIC_STRAVA_CLIENT_ID=seu_client_id
NEXT_PUBLIC_STRAVA_REDIRECT_URI=https://yourdomain.com/auth/callback

# Backend API
NEXT_PUBLIC_API_BASE_URL=https://xxxxx.execute-api.us-east-1.amazonaws.com/prod

# Analytics (opcional)
NEXT_PUBLIC_GA_ID=G-XXXXXXX
```

---

## 🚀 Deploy Checklist

- [ ] Frontend (`portfolio-site`) deployado no Vercel/CloudFront
- [ ] Backend (`lambda-backend`) deployado com `serverless deploy`
- [ ] DynamoDB tables criadas automaticamente
- [ ] Strava OAuth credentials configuradas
- [ ] Variáveis de ambiente atualizadas
- [ ] CORS configurado corretamente
- [ ] SSL/HTTPS habilitado
- [ ] CloudWatch logs monitorizados
- [ ] Testes E2E passando
- [ ] Documentação atualizada

---

## 📞 Troubleshooting

### CORS Error

**Problema:** "Access to XMLHttpRequest blocked by CORS policy"

**Solução:**
```bash
# Verificar serverless.yml
functions:
  getAthlete:
    events:
      - http:
          cors:
            origins:
              - 'https://yourdomain.com'
            headers:
              - Authorization
              - Content-Type
```

### Token Expired

**Problema:** 401 Unauthorized

**Solução:** Lambda automaticamente renova token. Se persistir, verificar:
```bash
# Verificar refresh_token no DynamoDB
aws dynamodb get-item \
  --table-name strava-users \
  --key '{"user_id":{"S":"123456"}}'
```

### Slow Performance

**Problema:** Respostas lentas

**Solução:**
- Aumentar Lambda memory: `memorySize: 1024`
- Verificar cold starts em CloudWatch
- Aumentar cache TTL

---

## 📚 Referências

- [Next.js Docs](https://nextjs.org/docs)
- [AWS Lambda](https://docs.aws.amazon.com/lambda/)
- [Strava API](https://developers.strava.com/)
- [DynamoDB](https://docs.aws.amazon.com/dynamodb/)
