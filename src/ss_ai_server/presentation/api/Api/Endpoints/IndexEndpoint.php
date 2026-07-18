<?php
/**
 * Index endpoint for the AI Server API.
 *
 * @package SS_AI_Image_Search
 * @subpackage Api
 */

declare( strict_types=1 );

namespace SS_AI_Image_Search\Api\Endpoints;

use SS_AI_Image_Search\Api\Client;
use SS_AI_Image_Search\Api\Response;
use SS_AI_Image_Search\Exceptions\Api\ApiException;

/**
 * Index endpoint class for indexing operations.
 */
class IndexEndpoint {

	/**
	 * API Client instance.
	 *
	 * @var Client
	 */
	private Client $client;

	/**
	 * Constructor.
	 *
	 * @param Client $client API Client instance.
	 */
	public function __construct( Client $client ) {
		$this->client = $client;
	}

	/**
	 * Index a single product.
	 *
	 * @param int   $product_id Product ID to index.
	 * @param array $params Additional indexing parameters.
	 * @return Response Response object.
	 * @throws ApiException If request fails.
	 */
	public function index_product( int $product_id, array $params = array() ): Response {
		$endpoint = 'index/product';

		$data = array(
			'product_id' => $product_id,
		);

		// Merge additional parameters.
		$data = array_merge( $data, $params );

		return $this->client->post( $endpoint, $data );
	}

	/**
	 * Index multiple products.
	 *
	 * @param array $product_ids Array of product IDs to index.
	 * @param array $params Additional indexing parameters.
	 * @return Response Response object.
	 * @throws ApiException If request fails.
	 */
	public function index_products( array $product_ids, array $params = array() ): Response {
		$endpoint = 'index/products';

		$data = array(
			'product_ids' => $product_ids,
		);

		// Merge additional parameters.
		$data = array_merge( $data, $params );

		return $this->client->post( $endpoint, $data );
	}

	/**
	 * Index all products.
	 *
	 * @param array $params Additional indexing parameters.
	 * @return Response Response object.
	 * @throws ApiException If request fails.
	 */
	public function index_all( array $params = array() ): Response {
		$endpoint = 'index/all';

		return $this->client->post( $endpoint, $params );
	}

	/**
	 * Delete a product from the index.
	 *
	 * @param int $product_id Product ID to delete.
	 * @return Response Response object.
	 * @throws ApiException If request fails.
	 */
	public function delete_product( int $product_id ): Response {
		$endpoint = 'index/product';

		$query_params = array(
			'product_id' => $product_id,
		);

		return $this->client->delete( $endpoint, $query_params );
	}

	/**
	 * Delete multiple products from the index.
	 *
	 * @param array $product_ids Array of product IDs to delete.
	 * @return Response Response object.
	 * @throws ApiException If request fails.
	 */
	public function delete_products( array $product_ids ): Response {
		$endpoint = 'index/products';

		$data = array(
			'product_ids' => $product_ids,
		);

		return $this->client->post( $endpoint, $data );
	}

	/**
	 * Clear the entire index.
	 *
	 * @return Response Response object.
	 * @throws ApiException If request fails.
	 */
	public function clear_index(): Response {
		$endpoint = 'index/clear';

		return $this->client->post( $endpoint );
	}

	/**
	 * Get indexing status.
	 *
	 * @param int|null $job_id Optional job ID to check.
	 * @return Response Response object.
	 * @throws ApiException If request fails.
	 */
	public function get_status( ?int $job_id = null ): Response {
		$endpoint = 'index/status';

		$query_params = array();

		if ( null !== $job_id ) {
			$query_params['job_id'] = $job_id;
		}

		return $this->client->get( $endpoint, $query_params );
	}

	/**
	 * Reindex all products.
	 *
	 * @param array $params Additional reindexing parameters.
	 * @return Response Response object.
	 * @throws ApiException If request fails.
	 */
	public function reindex( array $params = array() ): Response {
		$endpoint = 'index/reindex';

		return $this->client->post( $endpoint, $params );
	}
}