export interface CreateOrderRequest {
  customer_name: string;
  customer_email: string;
  package_tier_id: string;
  quantity?: number;
}

export interface CreateOrderResponse {
  payment_url: string;
  order_id: string;
  expires_at: string;
  status: string;
}

export type PlanType = 'explorer' | 'connector' | 'global_citizen';

// Mapping from Frontend Plan to Backend Package Tier ID
const PLAN_MAPPING: Record<PlanType, string> = {
  explorer: 'pkg_global_1gb_30d_tier1',       // 1GB Global
  connector: 'pkg_global_3gb_30d_tier1',      // 3GB Global
  global_citizen: 'pkg_global_5gb_30d_tier1', // 5GB Global
};

export async function createOrder(
  plan: PlanType,
  userDetails: { name: string; email: string }
): Promise<CreateOrderResponse> {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;
  if (!apiUrl) {
    throw new Error('NEXT_PUBLIC_API_URL is not defined');
  }

  const packageTierId = PLAN_MAPPING[plan];
  if (!packageTierId) {
    throw new Error(`Invalid plan type: ${plan}`);
  }

  const response = await fetch(`${apiUrl}/api/b2c/orders/auto-create`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      customer_name: userDetails.name,
      customer_email: userDetails.email,
      package_tier_id: packageTierId,
      quantity: 1,
    }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to create order');
  }

  return response.json();
}
