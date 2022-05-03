import matplotlib.pyplot as plt
import shapely.geometry
import shapely.wkt
import shapely.ops

# Defining original shapes
b1 = shapely.wkt.loads('LINESTRING (560546.12 6057255.286407334, 560545.3077266514 6057255.836198484, 560540.56200437 6057258.2789828135, 560535.6629350807 6057260.216576667, 560530.6613599712 6057261.784216983, 560525.5969426981 6057263.116654403, 560520.4895410759 6057264.338974588, 560515.3319056678 6057265.560578672, 560510.086238143 6057266.870712825, 560504.6859899524 6057268.335234894, 560499.0445254421 6057269.993517232, 560493.0681391365 6057271.858040347, 560486.6736334173 6057273.913701355, 560479.8057611532 6057276.120905187, 560472.4516402794 6057278.422070077, 560464.6492396847 6057280.748900355, 560456.4877151543 6057283.033326464, 560448.0995930482 6057285.217037817, 560439.6464209125 6057287.259478493, 560431.3002152538 6057289.142558624, 560423.2254101641 6057290.871111962, 560415.5630184817 6057292.469828505, 560408.4198559145 6057293.977093298, 560401.8644091389 6057295.4375603385, 560395.9281311083 6057296.894846845, 560390.6106741516 6057298.385719112, 560385.8888255056 6057299.936333202, 560381.7251632247 6057301.560916839, 560378.0755125153 6057303.262422995, 560374.8957934058 6057305.034736536, 560372.1453619355 6057306.865665564, 560369.7886465787 6057308.740059327, 560367.7953991884 6057310.642569412, 560366.1394116441 6057312.559415967, 560364.7977707094 6057314.479465343, 560363.7503617608 6057316.394364138, 560362.9787255703 6057318.297651781, 560362.4663575166 6057320.1846174225, 560362.2000627333 6057322.050779273, 560362.1699092751 6057323.891241297, 560362.3704026265 6057325.700602854, 560362.8015991225 6057327.473288741, 560363.4701709739 6057329.203315701, 560364.3899685831 6057330.8855618825, 560365.582559946 6057332.516387803, 560367.0760504204 6057334.094349552, 560368.9048957354 6057335.620848393, 560371.1070377725 6057337.1008109255, 560373.7202694931 6057338.543283372, 560376.7779140482 6057339.962371494, 560380.3024053206 6057341.377022076, 560384.3000158143 6057342.812221701, 560388.7561336465 6057344.298412045, 560393.6317907061 6057345.870769865, 560398.8629820239 6057347.567255063, 560404.3631893182 6057349.425507396, 560410.0291311903 6057351.478790639, 560415.7500327677 6057353.751616455, 560421.4173320535 6057356.255677785, 560426.9362210849 6057358.987243233, 560432.2348088761 6057361.926428135, 560437.2702637108 6057365.03862782, 560442.0307216174 6057368.277722234, 560446.5323099116 6057371.5903744325, 560450.8127548401 6057374.920611991, 560454.9218733545 6057378.213253872, 560458.9122819843 6057381.416732539, 560462.8313008943 6057384.484849961, 560466.7157573601 6057387.377777393, 560470.5902007747 6057390.064169144, 560474.4681462592 6057392.52363001, 560475.317585924 6057393.01)')
b2 = shapely.wkt.loads('LINESTRING (560546.12 6057370.350972405, 560545.6470436527 6057369.916491661, 560542.9769345002 6057367.767264656, 560540.3201695259 6057365.935868538, 560537.6525419411 6057364.404790053, 560534.9374870269 6057363.142207704, 560532.1319788088 6057362.10182235, 560529.1941878558 6057361.222048495, 560526.0919366574 6057360.428627199, 560522.8112714966 6057359.637927896, 560519.3641960851 6057358.7605487695, 560515.7941477832 6057357.708593233, 560512.1778247678 6057356.401723861, 560508.623207543 6057354.77570001, 560505.2635616962 6057352.788729845, 560502.246695547 6057350.426118524, 560499.7221411315 6057347.702147797, 560497.8267944445 6057344.658363443, 560496.6716553018 6057341.35867958, 560496.3319254743 6057337.8825400155, 560496.840798038 6057334.316158251, 560498.1900595294 6057330.746039137, 560500.3340861088 6057327.252561627, 560503.1979413652 6057323.906407781, 560506.6868130703 6057320.766775662, 560510.695186429 6057317.881076127, 560515.11428228 6057315.285270318, 560519.8370955654 6057313.0041574845, 560524.7611403409 6057311.051231846, 560529.7895712908 6057309.428146605, 560534.8320321282 6057308.123767292, 560539.8046092986 6057307.114502068, 560544.631798008 6057306.364487282, 560546.12 6057306.191368092)')
t1 = shapely.wkt.loads('LINESTRING (560466.2433944914 6057280.273491841, 560504.4746828988 6057322.757469366)')
t2 = shapely.wkt.loads('LINESTRING (560430.8944321264 6057361.182906415, 560496.6716553018 6057341.35867958)')

# Creating a union of all inputs. Also buffering all inputs to
# guarantee intersections across all lines.
buffer_size = 1
buff_union = shapely.ops.unary_union([b1.buffer(buffer_size),
                                      b2.buffer(buffer_size),
                                      t1.buffer(buffer_size),
                                      t2.buffer(buffer_size)])

# If the command above fails, try union first and then buffer:
# buff_union = shapely.ops.unary_union([b1,b2,t1,t2]).buffer(buffer_size)
print(type(buff_union))
# Extracting all the interior geometries
# Idea taken from here: https://stackoverflow.com/a/21922058/8667016
all_internal_geoms = [geom for geom in buff_union.interiors]

# Fishing out the interior geometry we really need
internal_geom = all_internal_geoms[0]

# Plotting results
# Code taken from here: https://stackoverflow.com/a/56140178/8667016
plt.plot(*internal_geom.xy)