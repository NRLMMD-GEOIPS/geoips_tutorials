# Future of GeoIPS
### Gwyn Uttmark (CIRA)

# Future of GeoIPS

- Procflow Overhaul
- Easier Install
- Cloud-native
- Making Things Simple
- Paralelization, GPU and ML Support
- Beyond 2-Dimensions

## Order Based Procflow

We're switching from the single procflow and the data fusion procflow to the **Order Based Procflow (OBP)**. This represents a major improvement in our ability to synthesize many different types of data and inputs into a workflow.

### Why things are the way they are
- Previously: Single source of data input with heuristic-based checks (described as a "plinko machine")
- Now: Order-based specification in YAML that runs steps in "order"
- Much more flexible and reflective of how meteorological data can be processed today

``` yaml
interface: workflows
family: order_based
name: order_based_IR_BD
docstring: |
  The IR_BD default configuration.
spec:
  steps:
    interpolator:
      kind: interpolator
      name: interp_nearest
      arguments: {}
    algorithm:
      kind: algorithm
      name: single_channel
      arguments:
        output_data_range: [-90.0, 40.0]
        input_units: Kelvin
        output_units: celsius
        min_outbounds: crop
        max_outbounds: crop
        norm: null
        inverse: null
    output_formatter:
      kind: output_formatter
      name: imagery_annotated
      arguments:
        colormapper:
          kind: colormapper
          name: IR_BD
          arguments:
            data_range: [-90.0, 40.0]
        filename_formatter:
          kind: filename_formatter
          name: geoips_fname
          arguments:
            suffix: ".png"
```

### Why
- **Idiomatic and clear**: "What you see is what you get"
- **Backwards compatible**: Mechanisms to translate existing procflows
- **Supports complex workflows**: Multiple inputs → multiple outputs
- **Eliminates black box processing**: No more (or fewer at least) invisible heuristics
- **Cloud-native eventually**: Designed with cloud deployment in mind

## Install

```bash
pip install geoips
```
- No need to clone repo for basic usage
- Non-editable mode installation
- Only need repo clone if developing core functionality

**Plugin Installation**
```bash
pip install geoips-plugin-name geoips_clavrx geoips_data_fusion
```

**End users can simply**
```bash
pip install geoips your-magical-weather-package
```
And have a complete working solution.

### Docker
- Development Docker image available now
- Dockerfile with multiple build stages
- Seeking feedback on dockerization needs

**Goals:**
- Smaller images for cloud-native applications
- Reduced dependencies for minimal deployments
- Clearer file organization
- Fewer installation steps



## Cloud-native

Moving toward deployment where **installing GeoIPS locally isn't even necessary**.

**Benefits:**
- Scalability
- Division of concerns
- Service-based architecture

## Infrastructure

- On-prem/remote Kubernetes
- Docker Swarm
- Other clustering services, pick your poison
- Quick AWS/Azure/Google Cloud cluster deployment

**GeoIPS Driver (Open Source):**
- File watcher
- File database
- Job dispatcher/query system
- Complete clustered workflow deployment

## Making Things Simple

**Current:**
```bash
# Current command (complex)
geoips run single_source $GEOIPS_TESTDATA_DIR/test_data_noaa_aws/data/goes16/20200918/1950/* \
  --procflow single_source \
  --reader_name abi_netcdf \
  --product_name geocolor \
  --compare_path $GEOIPS_PACKAGES_DIR/geoips/tests/outputs/abi.tc.geocolor \
  --output_formatter imagery_annotated \
  --filename_formatter tc_fname \
  --resampled_read \
  --sector_list tc2020al20laura
```


## Sometimes you need simple
```bash
geoips create geocolor data_files/*
```

### Configuration
- **Config file implementation**: Replace multiple environment variables
- **Sane defaults**: Works out-of-the-box for basic use cases
- **Better documentation**: Live, internet-accessible documentation
- **Training partnerships**: Working with experts at CIRA

### Philosophy
- Simple for daily use
- Order-based procflow for operational complexity
- Clear documentation for advanced options

## Paralelization, GPU and ML Support

- Consistent interfaces across different computational backends
- Cloud-native parallelization tools

### Parallelization
- Cluster/cloud-native deployment focused
- Consistent and controllable resource usage
- Avoid "bursty" usage patterns (1 core → 30 cores → 1 core)
- Our goal is steady resource usage (e.g., consistent 4-core usage)

### GPU Support:
- Already supports GPU-heavy algorithms
- Example: Temporal interpolation work by Jason Apke at CIRA
- Providing better guidance for GPU tooling setup

### Machine Learning Support
- Product generation for ML model training
- Data augmentation with labels
- Real-time validation metrics
- Integration with training workflows

## Beyond 2-Dimensions

- Typicaly: 2D spatial + 1D temporal data (satellite imagery)
- Possible but somewhat difficult: Higher dimensional data

**But there's so much more...**
- **3D spatial + 1D temporal**: Volume data over time
- **2D spatial + 2D temporal**: Time series imagery
- **Hyperspectral**: 2D spatial + spectral dimensions
- **Spectrum files**: 1D spatial, 0D temporal
- **Arbitrary n-dimensional data**

```python
# Instead of separate interpolators for each dimension
interpolate_2d(data_xobj)
interpolate_3d(data_xobj)
interpolate_4d(data_xobj)

# Single interface with metadata awareness
interpolate(data_xobj)  # Handles multiple dimensionalities
```

- Metadata-aware processing (don't interpolate time with space)
- Transparent algorithm support
- Coherent interface across dimensions
- Support for complex data structures
- Easy-to-use n-dimensional output formatters

## Validation

**Real-time Quality Metrics:**
- Percentage cloud coverage validation
- Clear sky/ocean percentage checks
- Sanity value checking (avoid 110% cloud, -5% ocean)
  
**Cross-platform Validation:**
- **EarthCARE integration**: LIDAR/radar cloud depth/height data
- Compare against CLAVRX outputs
- Connecting procflow loops with validation

**Validation Products:**
- Not operational products, but validation outputs
- Quality level assessment
- Performance monitoring
- "Tighten the loop" feedback system

**New Interfaces:**
- Dedicated validation interface
- Simplified validation product creation
- Automated quality assessment tools

## Testing

**Recent Improvements:**
- More efficient test execution
- Reduced test data requirements (small sectors vs. full disk/CONUS)
- Increased continuous integration testing
- More Python unit tests

**Future Goals:**
- **95% line coverage**: Most of GeoIPS code touched by tests
- **Faster integration tests**: 
  - Tokenizing and hashing
  - In-memory comparisons
  - Reduced pixel-by-pixel image comparisons

**Tooling Development:**
- Meteorological data testing tools
- Faster, more efficient testing workflows
- Better test data management

**We're especially interested in feedback on:**
- Dockerization requirements
- Parallelization needs  
- GPU workflows
- Cloud-native deployments

**Now is the time to speak up** - our roadmaps are still flexible!
