# Prática de SLAM 2D com `slam_toolbox` e Análise de Ruído Sensorial

**Autor:** Aurélio Batista Maciel Filho  
**Matrícula:** 20190179872

---

## 1. Ambiente de Simulação e Configuração

Os experimentos foram executados no simulador Gazebo com um ambiente composto por quatro obstáculos distintos (duas caixas, um cilindro e uma esfera). O mapeamento foi realizado em tempo real utilizando o pacote `slam_toolbox` (`online_async_launch.py`) em conjunto com teleoperação via teclado (`teleop_twist_keyboard`) e visualização no RViz.

---

## 2. Exercício 2.1 e 2.2 — Impacto do Ruído no Mapeamento (SLAM)

Para avaliar a robustez do algoritmo de SLAM, o mesmo cenário foi mapeado sob três configurações distintas de ruído nos sensores:

### Cenário 1: Sem ruído (Odometria e Lidar 2D *groundtruth*)
* **Configuração:** Desvio padrão do ruído do sensor laser zerado (`stddev = 0.0`) no `robot.urdf` e transformação `odom -> base_link` publicada diretamente pelo plugin diferencial (`diff_drive`).
* **Análise:** O mapa resultante apresenta contornos geométricos limpos, finos e bem definidos, tanto nas faces retas das caixas quanto na curvatura do cilindro. Como não há incerteza nas medições nem deriva na estimação de pose, o alinhamento das varreduras (*scan matching*) ocorre sem distorções.

### Cenário 2: Ruído apenas no Lidar 2D e Odometria *groundtruth*
* **Configuração:** Ruído Gaussiano ativado no sensor laser (`mean = 0.0`, `stddev = 0.03` m), mantendo a odometria *groundtruth*.
* **Análise:** A estrutura global do mapa permanece fiel às dimensões reais do ambiente porque a pose do robô é exata. Contudo, as paredes e superfícies dos obstáculos exibem dispersão granular ("efeito serrilhado" ou pontos espalhados ao redor das bordas reais) devido à variância nas leituras de distância do Lidar.

### Cenário 3: Ruído na Odometria e no Lidar 2D
* **Configuração:** Ruído Gaussiano mantido no Lidar (`stddev = 0.03` m) combinado com a publicação da transformação `odom -> base_link` pelo Filtro de Kalman Estendido (`ekf_filter_node`) fundindo odometria das rodas e IMU com ruído (`stddev = 0.1`), sem auxílio de GPS (*dead reckoning* puro).
* **Análise:** Este cenário apresenta a maior degradação na qualidade do mapa. O erro acumulado na estimação incremental de deslocamento e rotação (*drift* odiométrico) introduz desalinhamentos angulares e translacionais entre varreduras consecutivas, resultando em bordas mais espessas e sobreposições parciais nos contornos dos quatro obstáculos.

---

## 3. Exercício 3.1 — Problema do Robô Sequestrado (*Kidnapped Robot*)

* **Procedimento:** Com o mapa previamente construído no Cenário 3, a simulação foi pausada no Gazebo, o robô foi teletransportado manualmente para o extremo oposto do cenário utilizando a ferramenta de translação, e a simulação foi retomada.
* **Análise e Conclusão:** Após o teletransporte, o sistema **não foi capaz de recuperar automaticamente sua localização global correta**. Isso ocorre porque:
  1. A odometria e a IMU fornecem apenas estimativas propriocetivas relativas (*dead reckoning*), não registrando deslocamentos externos abruptos sem movimento das rodas;
  2. O `slam_toolbox` em modo de mapeamento contínuo realiza otimização local (*scan-to-map matching*) ancorada na última pose estimada pela odometria;
  3. Sem um módulo de relocalização global ativa (como espalhamento global de partículas ou reconhecimento imediato de fechamento de ciclo), o robô assume que permanece na vizinhança da pose anterior e passa a projetar as novas leituras do Lidar na região incorreta do mapa.

---

## 4. Evidências (Capturas de Ecrã)

As imagens correspondentes a cada etapa encontram-se organizadas na pasta compartilhada do Google Drive:
1. `18:54` — Mapeamento com ruído apenas no Lidar 2D (Exercício 2.1 / Cenário 2).
2. `19:06` — Mapeamento sem ruído / *groundtruth* (Exercício 2.2 / Cenário 1).
3. `19:29` — Mapeamento com ruído na odometria e no Lidar 2D (Exercício 2.2 / Cenário 3).
4. `19:31` — Simulação do problema do Robô Sequestrado no Gazebo e RViz (Exercício 3.1).
