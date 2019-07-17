## AEROSOL MODE AND SPECIES PROPERTIES

# Define names of modes
mode_names <- c("accu", "aitk", "coarse", "porg")

# Assign sigma (fixed width of lognormal bin) for each mode. [-]
# (see Liu et al., 2016; physprops files)
sigma_g <- c(1.8, 1.6, 1.8, 1.6)

# Assign minimum and maximum dry geometric mean diameter for each mode [m]
# (see Liu et al., 2016; physprops files)

# Lower bound
dgnumlo <- c(5.35e-8, 8.70e-9, 1.00e-6, 1.00e-8)

# Upper bound
dgnumhi <- c(4.40e-7, 5.20e-8, 4.00e-6, 1.00e-7)

# Default/nominal value of dgnum for each mode? (can get from physprops file)


# Default volume-to-number ratio for each mode? (can get from physprops file)

# Density of aerosol components as assigned in the model [kg m^-3]
density_mom <- 1601.
density_ncl <- 1900.
density_pom <- 1000.
density_soa <- 1000.
density_so4 <- 1770.
density_dst <- 2600.
density_bc  <- 1700.

# Hygroscopicity of aerosol components as assigned in the model [-]
kappa_mom <- 0.1
kappa_ncl <- 1.16
kappa_pom <- 1.0e-10
kappa_soa <- 0.14
kappa_so4 <- 0.507
kappa_dst <- 0.068
kappa_bc  <- 1.0e-10

# Set OM:OC ratio
OM_to_OC = 1.9 # for marine organics
OM_to_OC_soa = 1.9 # For consistency
OM_to_OC_poa = 1.9 # For consistency
#OM_to_OC_poa = 1.4 # e.g. Aiken et al., 2008
