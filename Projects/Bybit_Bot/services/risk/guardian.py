import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RiskGuard")

class RiskGuard:
    """
    Service D: Risk Guard (Риск-менеджер)
    Middleware, который проверяет каждый ордер ДО отправки.
    """
    def __init__(self, max_leverage=3, max_pos_size=1000, daily_loss_limit=500):
        self.max_leverage = max_leverage
        self.max_pos_size = max_pos_size
        self.daily_loss_limit = daily_loss_limit
        self.current_daily_loss = 0

    def validate_order(self, order_data):
        """
        order_data: {
            'symbol': 'BTCUSDT',
            'side': 'Buy',
            'amount': 0.01,
            'leverage': 1,
            'price': 100000
        }
        """
        # 1. Проверка плеча
        if order_data['leverage'] > self.max_leverage:
            logger.error(
                f"❌ Плечо {order_data['leverage']} превышает "
                f"лимит {self.max_leverage}"
            )
            return False

        # 2. Проверка размера позиции (Notional Value)
        notional_value = order_data['amount'] * order_data['price']
        if notional_value > self.max_pos_size:
            logger.error(
                f"❌ Размер позиции ${notional_value} превышает "
                f"лимит ${self.max_pos_size}"
            )
            return False

        # 3. Kill Switch (Дневной убыток)
        if self.current_daily_loss >= self.daily_loss_limit:
            logger.critical("🛑 KILL SWITCH: Дневной лимит убытка достигнут!")
            return False

        logger.info(
            f"✅ Ордер валидирован: {order_data['symbol']} "
            f"{order_data['side']} {order_data['amount']}"
        )
        return True

if __name__ == "__main__":
    guard = RiskGuard()
    test_order = {
        'symbol': 'BTCUSDT', 'side': 'Buy', 'amount': 0.1,
        'leverage': 1, 'price': 100000
    }
    guard.validate_order(test_order)
