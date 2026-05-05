import "@specodec/typespec-emitter-core";
using Specodec.Core;

namespace MyNS {
  @specodec model Foo { x: int32; }
  namespace inner {
    @specodec model Bar { y: string; }
    namespace deep {
      @specodec model Baz { z: float64; }
    }
  }
}
