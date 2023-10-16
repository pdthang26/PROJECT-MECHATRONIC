#include "SR04.h"


void Init_SR04x(SR04_Name* SR04_x,TIM_HandleTypeDef *htim, TIM_TypeDef* TIMx, GPIO_TypeDef* GPIOx_trig, uint16_t pinTrig, GPIO_TypeDef* GPIOx_echo,uint16_t pinEcho)
{
	SR04_x->htim_SR04 = htim;
	SR04_x->TIMx = TIMx;
	SR04_x->GPIOx_TRIG = GPIOx_trig;
	SR04_x->GPIOx_ECHO = GPIOx_echo;
	SR04_x->PIN_TRIG = pinTrig;
	SR04_x->PIN_ECHO = pinEcho;
}

void readPulseDurationSR04 (SR04_Name* SR04_x,uint32_t timeout)
{
	HAL_TIM_Base_Stop(SR04_x->htim_SR04);
	(SR04_x->TIMx)->CNT = 0;
	uint32_t startTime = HAL_GetTick();
  uint32_t timeoutTime = startTime + timeout;
  uint32_t lastTime;
  uint32_t pulse = 0;
  uint32_t inputState = 0;
	uint32_t pulseWidth=0;
    
    if (state == 1)
    {
        inputState = GPIO_PIN_SET;
    }
    else if (state == 0)
    {
        inputState = GPIO_PIN_RESET;
    }
		
		HAL_GPIO_WritePin(SR04_x->GPIOx_TRIG, SR04_x->PIN_TRIG,1);
		HAL_TIM_Base_Start(SR04_x->htim_SR04);
		while((SR04_x->TIMx) ->CNT <= 10);
		HAL_GPIO_WritePin(SR04_x->GPIOx_TRIG, SR04_x->PIN_TRIG,0);
		
		HAL_TIM_Base_Stop(SR04_x->htim_SR04);
		(SR04_x->TIMx)->CNT = 0;
		
    
    while (HAL_GPIO_ReadPin(SR04_x->GPIOx_ECHO, SR04_x->PIN_ECHO) != inputState)
    {
        if (HAL_GetTick() > timeoutTime)
        {
            SR04_x ->pulseValue = 0;
        }
    }
    
    HAL_TIM_Base_Start(SR04_x->htim_SR04);
    while (HAL_GPIO_ReadPin(SR04_x->GPIOx_ECHO, SR04_x->PIN_ECHO) == inputState)
    {
        if (HAL_GetTick() > timeoutTime)
        {
            SR04_x ->pulseValue = 0;
        }
    }
    SR04_x ->pulseValue  = (SR04_x->TIMx)->CNT ;
		HAL_TIM_Base_Stop(SR04_x->htim_SR04);
		(SR04_x->TIMx)->CNT = 0;
	
	
}

uint32_t pulseIn(uint32_t pin, uint32_t state, uint32_t timeout)
{
    uint32_t startTime = HAL_GetTick();
    uint32_t timeoutTime = startTime + timeout;
    uint32_t lastTime;
    uint32_t pulse = 0;
    uint32_t inputState = 0;
		uint32_t pulseWidth=0;
    
    if (state == 1)
    {
        inputState = GPIO_PIN_SET;
    }
    else if (state == 0)
    {
        inputState = GPIO_PIN_RESET;
    }
    
    while (HAL_GPIO_ReadPin(GPIOA, pin) != inputState)
    {
        if (HAL_GetTick() > timeoutTime)
        {
            return 0;
        }
    }
    
    lastTime = TIM2->CNT;
    
    while (HAL_GPIO_ReadPin(GPIOA, pin) == inputState)
    {
        if (HAL_GetTick() > timeoutTime)
        {
            return 0;
        }
    }
    
    pulse = TIM2->CNT - lastTime;
		
    return pulse;
}